import os
from importlib.util import find_spec


def _find_qt_api() -> str:
    """
    this should be called before importing qtpy.
    refer: `lib:qtpy/__init__.py`
    """
    api = os.getenv('QT_API', '')
    
    if not api:
        for pkg, api in {
            'PySide6'     : 'pyside6',
            'PyQt6'       : 'pyqt6',
            'PySide2'     : 'pyside2',
            'PyQt5'       : 'pyqt5',
            'pyside6_lite': 'pyside6_lite'
        }.items():
            if find_spec(pkg):
                print(':v2', f'auto detected qt api: {api}')
                os.environ['QT_API'] = api
                break
        else:
            raise ModuleNotFoundError('no qt bindings found!')
    
    if api == 'pyside6_lite':
        # see `sidework/pyside_package_tailor/dist/pyside6_lite`.
        # activate special pyside6 location.
        import pyside6_lite  # noqa
        # set environ to be 'pyside6' for qtpy to recognize it.
        os.environ['QT_API'] = 'pyside6'
    
    elif api == 'pyside2':
        # try to repair pyside2 highdpi issue
        #   https://www.hwang.top/post/pyside2pyqt-zai-windows-zhong-tian-jia
        #   -dui-gao-fen-ping-de-zhi-chi/
        # warning: this must be called before QCoreApplication is created.
        from PySide2 import QtCore  # noqa
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    
    return api


def _get_qt_version() -> float:
    """
    return <major>.<minor> version of the qt api.
    """
    from qtpy import QT_VERSION  # e.g. '5.15.2'
    return float('.'.join(QT_VERSION.split('.')[:2]))


IS_WINDOWS: bool = os.name == 'nt'
QT_API: str = _find_qt_api()
QT_VERSION: float = _get_qt_version()
