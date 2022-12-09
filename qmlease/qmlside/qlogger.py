from os import name as os_name

from lk_logger.path_helper import path_helper
from lk_utils.filesniff import normpath
from qtpy.QtCore import QMessageLogContext
from qtpy.QtCore import QtMsgType
from qtpy.QtCore import qInstallMessageHandler

try:
    from qtpy.QtCore import QtCriticalMsg
    from qtpy.QtCore import QtWarningMsg
except ImportError:
    # this may happen when we are using PySide6 >= 6.4.0
    from qtpy.QtCore import qCritical as QtCriticalMsg
    from qtpy.QtCore import qWarning as QtWarningMsg

SHOW_FUNCNAME = False
_IGNORE_UNPLEASENT_WARNINGS = False
_IS_WINDOWS = os_name == 'nt'


def setup(ignore_unpleasent_warnings=False):
    """ Print QML runtime info in Python (PyCharm) console.
    
    Motivation:
        In traditional way when we are developing and debugging QML in PyCharm,
        we have to enable 'Toolbar > Edit Run/Debug configurations dialog >
        Emulate terminal in output console' to see `console.log(...)` via
        PyCharm console.
        The disadvantages are that the steps are trivial and enabling it will
        cause PyCharm console loses some features like code highlighting and
        linking etc.
        So we find another way to introduce qml to use the same output stream
        with python print. Just call this function and all work is done.
        
    Notes:
        Call this function before application starts.
    """
    global _IGNORE_UNPLEASENT_WARNINGS
    _IGNORE_UNPLEASENT_WARNINGS = ignore_unpleasent_warnings
    qInstallMessageHandler(_log)


# noinspection PyUnusedLocal
def _log(mode: QtMsgType, ctx: QMessageLogContext, msg: str) -> None:
    """
    Features:
        1. Output stream via PyCharm console.
        2. Support source map print.
    
    References:
        https://stackoverflow.com/questions/53991306/pyside-how-to-see-qml
            -errors-in-python-console
        
    Args:
        mode: qtpy.QtCore.QtMsgType
            There're six message types:
                QtCriticalMsg  # 1
                QtDebugMsg
                QtFatalMsg
                QtInfoMsg
                QtSystemMsg
                QtWarningMsg  # 2
            #1 and #2 are what we mostly occurred.
        ctx: qtpy.QtCore.QMessageLogContext. (ctx: 'context')
            Context indicates to the place where `console.log` is called or
            where runtime errors happened.
            ctx.file: Optional[str].
                the abspath of file, starts with 'file:///', and usually ends
                with '.qml' or '.js'.
            ctx.line: int.
                the line number, starts from 1.
                sometimes it is -1.
            ctx.function: Optional[str].
                `None` means no function name.
            ctx.category: str.
                *don't know what it is, usually seen its value is 'default' or
                'qml'.*
            ctx.version: int.
                *don't know what it is, usually seen its value is integer 2.*
        msg: str. (msg: 'message')
        
    Returns:
        print: '{file}:{lineno}  >>  {function}  >>  {message}'
    """
    # print(':v', mode, ctx.file, ctx.line, ctx.function, msg)  # for debug
    
    # TEST
    if ctx.file == 'eval code':
        raise Exception('eval code')
    
    # filename
    filename = _reformat_path(ctx.file) if ctx.file else '<unknown_source>'
    
    if _IGNORE_UNPLEASENT_WARNINGS:
        if filename in (
                # https://forum.qt.io/topic/131823/lots-of-typeerrors-in-console
                # -when-migrating-to-qt6/2
                '<qrc:/qt-project.org/imports/QtQuick/Controls/'
                'macOS/Button.qml>',
        ):
            return
    
    # line number
    lineno = 0 if ctx.line == -1 else ctx.line
    
    # function
    function = ctx.function
    
    # optimize msg
    if mode in (QtWarningMsg, QtCriticalMsg):
        if ctx.file and msg.startswith(ctx.file):
            # examples:
            #   msg = '<ctx.file>: <message>'
            #   msg = '<ctx.file>:<line_no>:<column_no>: <message>'
            # so we firstly strip `ctx.file`, then split by ': ' to extract the
            # main message.
            msg = msg[len(ctx.file):].split(': ', 1)[1]
        msg = '\033[31m' + msg + '!' + '\033[0m'
        #   change font color to red, and add an exclamation mark to it.
    
    if SHOW_FUNCNAME and function:
        print(':s2', '{}:{}'.format(filename, lineno), ctx.function, msg)
    else:
        print(':s2', '{}:{}'.format(filename, lineno), msg)


def _reformat_path(path: str) -> str:
    """
    args:
        path: qml file path.
            currently we've found 2 forms:
                1. file:///c:/workspace/...
                2. c:%5Cworkspace%5C...
                     ^^^         ^^^
            warning:
                the path may contain '../' in its body part.
    return:
        a. the relative path to current working dir:
            ./view.qml
        b. a short form to third party (lib) dir:
            [xxx_lib]/view.qml
        c. unknown type
            <{path}>
    """
    if path.startswith('file:///'):
        if _IS_WINDOWS:
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
    
    path = normpath(path, force_abspath=True)
    
    if path_helper.is_external_lib(path):
        return path_helper.reformat_external_lib_path(
            path, style='pretty_relpath'
        )
    else:
        return path_helper.relpath(path)
