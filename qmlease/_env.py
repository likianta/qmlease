import os
import typing as tp


def _find_qt_api() -> str:
    """
    this should be called before importing qtpy.
    refer: `lib:qtpy/__init__.py`
    """
    if api := os.getenv('QT_API', '').lower():
        if api == 'pyside2':
            # try to repair pyside2 highdpi issue
            #   https://www.hwang.top/post/pyside2pyqt-zai-windows-zhong-tian
            #   -jia-dui-gao-fen-ping-de-zhi-chi/
            # warning: this must be called before QCoreApplication is created.
            from PySide2 import QtCore  # type: ignore

            QtCore.QCoreApplication.setAttribute(
                QtCore.Qt.AA_EnableHighDpiScaling
            )
        return api
    else:
        for pkg, api in {
            'PySide6': 'pyside6',
            'PyQt6': 'pyqt6',
            'PySide2': 'pyside2',
            'PyQt5': 'pyqt5',
        }.items():
            try:
                m = __import__(pkg)
            except ModuleNotFoundError:
                continue
            else:
                print(
                    ':v2',
                    'auto detected qt api: {} ({})'.format(
                        api, getattr(m, '__version__', 'version unknown')
                    ),
                )
                os.environ['QT_API'] = api
                return api
        else:
            raise ModuleNotFoundError('no qt bindings found!')


def _get_qt_version() -> tp.Tuple[int, int, int]:
    """
    return <major>.<minor> version of the qt api.
    """
    from qtpy import QT_VERSION  # e.g. '5.15.2'

    assert isinstance(QT_VERSION, str)
    assert QT_VERSION.count('.') == 2
    # noinspection PyTypeChecker
    return tuple(map(int, QT_VERSION.split('.')))  # type: ignore


IS_WINDOWS = os.name == 'nt'
QT_API = _find_qt_api()
QT_DEBUG = False
QT_VERSION = _get_qt_version()
