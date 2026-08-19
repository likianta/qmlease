import os
import re
import sys

import neoprint as np
from lk_utils import fs
from neoprint.path_scope import path_glob
from qtpy import QtCore
from qtpy.QtCore import QtMsgType

from ..application import app
from .._env import IS_WINDOWS
from ..qtcore import QObject

# print(':nl', QtCore.qDebug, QtCore.qInfo, QtCore.qWarning, QtCore.qCritical)
# print(
#     ':nl',
#     QtMsgType.QtSystemMsg,
#     QtMsgType.QtDebugMsg,
#     QtMsgType.QtInfoMsg,
#     QtMsgType.QtWarningMsg,
#     QtMsgType.QtCriticalMsg,
#     QtMsgType.QtFatalMsg,
# )

RAISE_EXCEPTION = os.getenv('QMLEASE_ZERO_TOLERANCE_EXCEPTION', '0') == '1'
SHOW_FUNCNAME = False
SHOW_UNPLEASENT_WARNINGS = os.getenv('QMLEASE_DEBUG', '0') == '1'
_BUILTIN_WIDGETS_DIR = fs.there('../widgets')
_CURRENT_WORKING_DIR = fs.normpath(os.getcwd())
_VENV_PACKAGES_DIR = fs.normpath(sys.exec_prefix + '/Lib/site-packages')


class Console(QObject):
    def __init__(self) -> None:
        super().__init__()
        self._file_id_map = {}
        #   dict[str id, tuple[str pretty_path, int start_line_no]]
        self._file_id_map_rev = {}
        self._file_id_pattern = re.compile(r'\[file_id:(\d+)]')
        self._simple_id_counter = 0
        QtCore.qInstallMessageHandler(self._handle_message)

    def generate_file_id(self, path: str, start_line_no: int) -> str:
        path = fs.normpath(path)
        if (path, start_line_no) in self._file_id_map_rev:
            return self._file_id_map_rev[(path, start_line_no)]
        self._simple_id_counter += 1
        file_id = str(self._simple_id_counter)
        self._file_id_map[file_id] = (
            # '[magenta]\\[qmlease][/]/' + self._reformat_path(path)[2:],
            #   e.g. 'd:/aaa/bbb.py' -> './bbb.py' -> '[qmlease]/bbb.py'
            self._reformat_path(path),
            start_line_no,
        )
        self._file_id_map_rev[(path, start_line_no)] = file_id
        return file_id

    def _handle_message(
        self, mode: QtMsgType, ctx: QtCore.QMessageLogContext, msg: str
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
        # print(':lnv', mode, ctx.file, ctx.line, ctx.function, msg)  # TEST
        # if ctx.file == 'eval code':
        #     raise Exception(msg)

        # file path
        if msg.startswith('[file_id:'):
            file_id = self._file_id_pattern.search(msg).group(1)  # type: ignore
            file_path, start_line_no = self._file_id_map[file_id]
            msg = '(qml) ' + msg.split(']', 1)[1]
        else:
            start_line_no = 0
            if ctx.file:
                # strip `<file>:<row>:<col>` prefix from `msg`.
                if msg.startswith(ctx.file):
                    assert msg.startswith(
                        prefix := '{}:{}: '.format(ctx.file, ctx.line)
                    )
                    msg = msg[len(prefix) :]

                file_path = self._normalize_path(ctx.file)
                file_path = self._reformat_path(file_path)
                if not SHOW_UNPLEASENT_WARNINGS:
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

                    if not IS_WINDOWS and (
                        'qrc:/qt-project.org/imports/QtQuick/Controls/macOS/'
                        in file_path
                    ):
                        # https://forum.qt.io/topic/131823/lots-of
                        # -typeerrors-in-console-when-migrating-to-qt6/2
                        return
            else:
                if not SHOW_UNPLEASENT_WARNINGS:
                    if msg == 'Retrying to obtain clipboard.':
                        return
                file_path = '<unknown>'

        line_number = 0 if ctx.line == -1 else ctx.line + start_line_no
        source = f'{file_path}:{line_number}'
        func_name = ctx.function

        if mode in (QtMsgType.QtWarningMsg, QtMsgType.QtCriticalMsg):
            np.print(
                '{} > {}'.format(source, msg),
                markup=':s1v{}'.format('6' if QtMsgType.QtWarningMsg else '8'),
            )
            if RAISE_EXCEPTION:
                app.force_exit()
        elif SHOW_FUNCNAME and func_name:
            np.print(
                '{} > {} > {}'.format(source, ctx.function, msg), markup=':s1'
            )
        else:
            np.print('{} > {}'.format(source, msg), markup=':s1')

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
        return fs.normpath(path, True)

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
        if path_glob.is_external_path(path):
            if path.startswith(_CURRENT_WORKING_DIR):
                return './' + path.removeprefix(_CURRENT_WORKING_DIR + '/')
            elif path.startswith(_VENV_PACKAGES_DIR):
                a, b = path.removeprefix(_VENV_PACKAGES_DIR + '/').split('/', 1)
                return '[{}]/{}'.format(a, b)
            else:
                return path
        else:
            assert path.startswith(_CURRENT_WORKING_DIR)
            return './' + path.removeprefix(_CURRENT_WORKING_DIR + '/')


qml_console = Console()
