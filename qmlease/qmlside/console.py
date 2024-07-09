import re

from lk_logger.path_helper import path_helper
from lk_utils import normpath
from lk_utils import xpath
from qtpy.QtCore import QMessageLogContext
from qtpy.QtCore import QtMsgType
from qtpy.QtCore import qInstallMessageHandler

from .._env import IS_WINDOWS
from .._env import QT_VERSION
from ..qtcore import QObject

if QT_VERSION >= 6.4:
    from qtpy.QtCore import qCritical as QtCriticalMsg
    from qtpy.QtCore import qWarning as QtWarningMsg
else:
    from qtpy.QtCore import QtCriticalMsg  # noqa
    from qtpy.QtCore import QtWarningMsg  # noqa

IGNORE_UNPLEASENT_WARNINGS = True
SHOW_FUNCNAME = False
_BUILTIN_WIDGETS_DIR = xpath('../widgets', True)


class Console(QObject):
    
    def __init__(self):
        super().__init__()
        self._file_id_map = {}
        #   dict[str id, tuple[str pretty_path, int start_line_no]]
        self._file_id_map_rev = {}
        self._file_id_pattern = re.compile(r'\[file_id:(\d+)]')
        self._simple_id_counter = 0
        qInstallMessageHandler(self._handle_message)
    
    def generate_file_id(self, path: str, start_line_no: int) -> str:
        path = normpath(path)
        if (path, start_line_no) in self._file_id_map_rev:
            return self._file_id_map_rev[(path, start_line_no)]
        self._simple_id_counter += 1
        file_id = str(self._simple_id_counter)
        self._file_id_map[file_id] = (
            # '[magenta]\\[qmlease][/]/' + self._reformat_path(path)[2:],
            #   e.g. 'd:/aaa/bbb.py' -> './bbb.py' -> '[qmlease]/bbb.py'
            self._reformat_path(path),
            start_line_no
        )
        self._file_id_map_rev[(path, start_line_no)] = file_id
        return file_id
    
    # noinspection PyUnresolvedReferences
    def _handle_message(
        self,
        mode: QtMsgType,
        ctx: QMessageLogContext,
        msg: str,
    ) -> None:
        """
        params:
            mode:
                QtMsgType.QtCriticalMsg
                QtMsgType.QtDebugMsg
                QtMsgType.QtFatalMsg
                QtMsgType.QtInfoMsg
                QtMsgType.QtSystemMsg
                QtMsgType.QtWarningMsg
            ctx:
                main properties:
                    ctx.file:
                        usual form: 'file:///<abspath>'
                        special case: 'eval code'
                    ctx.line: int, -1 for unknown line number.
                    ctx.function: func name or None.
            msg:
                special case 1:
                    `<ctx.file>:<ctx.line>:<column>: ...`
                special case 2:  TODO: explain this case
                    '[file_id:<id>]...'
        """
        # print(':v', mode, ctx.file, ctx.line, ctx.function, msg)  # TEST
        # if ctx.file == 'eval code':
        #     raise Exception(msg)
        
        # file path
        if msg.startswith('[file_id:'):
            file_id = self._file_id_pattern.search(msg).group(1)
            file_path, start_line_no = self._file_id_map[file_id]
            msg = '(qml) ' + msg.split(']', 1)[1]
        else:
            start_line_no = 0
            if ctx.file:
                # strip `<file>:<row>:<col>` prefix from `msg`.
                if msg.startswith(ctx.file):
                    msg = msg.replace(ctx.file, '', 1)
                    assert (m := re.match(r':\d+(?::\d+)?: ', msg)), msg
                    msg = msg[len(m.group()):]
                
                file_path = self._normalize_path(ctx.file)
                file_path = self._reformat_path(file_path)
                if IGNORE_UNPLEASENT_WARNINGS:
                    if (
                        'The current style does not support customization of '
                        'this control' in msg
                    ):
                        # pyside6 v6.6+, recorded at 2024-01-29
                        # the whole warning is (e.g.):
                        #   msg = file:///Users/Likianta/Desktop/workspace
                        #   /dev_master_likianta/qmlease/qmlease/widgets
                        #   /LKWidgets/Buttons/LKIconButton.qml:42:21: QML
                        #   QQuickItem: The current style does not support
                        #   customization of this control (property:
                        #   "background" item: QQuickItem(0x600002405c00,
                        #   parent=0x0, geometry=0,0 0x0)). Please
                        #   customize a non-native style (such as Basic,
                        #   Fusion, Material, etc). For more information,
                        #   see: https://doc.qt.io/qt-6/qtquickcontrols2
                        #   -customize.html#customization-reference
                        return
                    if not IS_WINDOWS:
                        if (
                            'qrc:/qt-project.org/imports/QtQuick/Controls'
                            '/macOS/' in file_path
                        ):
                            # https://forum.qt.io/topic/131823/lots-of
                            # -typeerrors-in-console-when-migrating-to-qt6/2
                            return
            else:
                file_path = '<unknown>'
        
        line_number = 0 if ctx.line == -1 else ctx.line + start_line_no
        source = f'{file_path}:{line_number}'
        func_name = ctx.function
        logger_markup = ':s1'
        
        # optimize msg
        if mode in (QtWarningMsg, QtCriticalMsg):
            if ctx.file and msg.startswith(ctx.file):
                # examples:
                #   msg = '<ctx.file>: <message>'
                #   msg = '<ctx.file>:<line_no>:<column_no>: <message>'
                # so we firstly strip `ctx.file`, then split by ': ' to extract
                # the main message.
                msg = msg[len(ctx.file):].split(': ', 1)[1]
            msg += '!'
            logger_markup = ':v4s1'
        
        # msg = msg.replace('[', '\\[')
        if SHOW_FUNCNAME and func_name:
            print('{}  >  {}  >  {}'.format(
                source, ctx.function, msg), logger_markup)
        else:
            print('{}  >  {}'.format(source, msg), logger_markup)
    
    @staticmethod
    def _normalize_path(path: str) -> str:
        """
        examples:
            file:///c:/aaa/bbb -> c:/aaa/bbb
            c:%5Caaa%5Cbbb -> c:/aaa/bbb
            c:%5Caaa%5C..%5Cbbb -> c:/bbb
            eval code -> <eval code>
        """
        if path.startswith('file:///'):
            if IS_WINDOWS:
                # e.g. 'file:///c:/workspace/...'
                path = path[8:]
            else:
                # e.g. 'file:///Users/...'
                path = path[7:]
        elif path.startswith('file://'):  # unix
            # e.g. 'file://users/...'
            path = '/' + path[7].upper() + path[8:]
        elif path[1:].startswith(':%5C'):
            path = path.replace('%5C', '/')
        else:
            return f'<{path}>'  # e.g. '<eval code>'
        return normpath(path, True)
    
    @staticmethod
    def _reformat_path(path: str) -> str:
        """
        return:
            a. the relative path to current working dir:
                ./view.qml
            b. a short form to third party (lib) dir:
                [xxx_lib]/view.qml
            c. unknown type
                <{path}>
        """
        if path.startswith('<'):
            return path
        return path_helper.get_relpath(path)


qml_console = Console()
