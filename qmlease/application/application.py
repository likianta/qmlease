from __future__ import annotations

import typing as t
from os.path import exists

from qtpy.QtCore import QObject
from qtpy.QtQml import QQmlApplicationEngine
from qtpy.QtQml import QQmlContext
from qtpy.QtWidgets import QApplication

from .register import Register
from ..qtcore import signal


class Application(QApplication):
    engine: QQmlApplicationEngine
    root: QQmlContext
    on_exit: signal
    _on_exit_funcs: t.List[t.Callable]
    _register: Register
    
    def __init__(self, app_name='QmlEase Demo', **kwargs):
        """
        Args:
            app_name: str
                set application name.
                the name can laterly be changed by calling `self.set_app_name`.
            kwargs:
                organization: str[default='dev.likianta.qmlease']
                    set an organization name, this avoids an error from
                    `QtQuick.Dialogs.FileDialog`.
                    note: what did the error look like?
                        QML Settings: The following application identifiers
                        have not been set: QVector("organizationName",
                        "organizationDomain")
        """
        super().__init__()
        
        self.setApplicationName(app_name)
        self.setOrganizationName(kwargs.get(
            'organization', 'dev.likianta.qmlease'
        ))
        
        self.engine = QQmlApplicationEngine()  # noqa
        self.root = self.engine.rootContext()
        self._on_exit_funcs = []
        self._register = Register(self.root)
        
        self._ui_fine_tune()
        
        from lk_utils import xpath
        self.register_qmldir(xpath('../widgets'))
        self.register_qmldir(xpath('../themes'))
        
        self.on_exit = super().aboutToQuit  # noqa
    
    def _ui_fine_tune(self) -> None:
        from os import name
        if name == 'nt':
            self.setFont('Microsoft YaHei UI')  # noqa
    
    # -------------------------------------------------------------------------
    
    def set_app_name(self, name: str) -> None:
        # just made a consistent snake-case function alias for external caller,
        # especially for who imports a global instance `app` from this module.
        self.setApplicationName(name)
    
    @staticmethod
    def set_assets_root(root_dir: str) -> None:
        from ..qmlside import pyassets
        pyassets.set_root(root_dir)
    
    # -------------------------------------------------------------------------
    
    def register_qmldir(self, qmldir: str) -> None:
        """
        args:
            qmldir:
                this directory should include at least one sub folder, which is
                available for qml to import.
                the sub folders should contain one 'qmldir' file, and multiple
                '*.qml' files. see example of './widgets_lib'.
        """
        if not exists(qmldir):
            print(':v3p', 'the qmldir not exists! it may cause a "xxx is not '
                          'installed" error in qml side.', qmldir)
        self.engine.addImportPath(qmldir)
    
    def register(
            self, qobj: QObject | type[QObject], name='', namespace='',
    ) -> None:
        self._register.register(qobj, name, namespace)
    
    def _register_backend(self) -> None:
        from ..pyside import pyside
        from ..qmlside import pyassets, pybroad, pyenum, pylayout
        from ..qmlside import widgets_backend as wb
        from ..style import pystyle
        
        self.register(pyassets, 'pyassets', 'global')
        self.register(pybroad, 'pybroad', 'global')
        self.register(pyenum, 'pyenum', 'global')
        self.register(pylayout, 'pylayout', 'global')
        self.register(pyside, 'pyside', 'global')
        self.register(pystyle, 'pystyle', 'global')
        self.register(pystyle.color, 'pycolor', 'global')
        self.register(pystyle.font, 'pyfont', 'global')
        self.register(pystyle.motion, 'pymotion', 'global')
        self.register(pystyle.size, 'pysize', 'global')
        
        self.register(wb.ListView(), 'lklistview', 'global')
        self.register(wb.Progress(), 'lkprogress', 'global')
        self.register(wb.ScopeEngine(), 'lkscope', 'global')
        self.register(wb.Slider(), 'lkslider', 'global')
        self.register(wb.util, 'lkutil', 'global')
        
        from lk_utils import xpath
        pyassets.add_source(xpath('../widgets'), 'lkwidgets')
    
    # -------------------------------------------------------------------------
    
    def run(self, qml_file: str, debug=False) -> None:
        self._register.freeze()
        if debug:
            from ..qmlside import HotReloader
            reloader = HotReloader(reload_scheme='clear_cache', app=app)
            reloader.run(qml_file)
        else:
            self._run(qml_file)
    
    def _run(self, qmlfile: str) -> None:
        """
        note: do not merge this method into `run`, because
        `..qmlside.HotReloader` internally uses this.
        """
        self._register_backend()
        
        from lk_utils import normpath
        self.engine.load('file:///' + normpath(qmlfile, force_abspath=True))
        
        self.on_exit.connect(self._exit)
        
        from os import getenv
        if getenv('QT_API') in ('pyside2', 'pyqt5'):
            self.exec_()
        else:
            self.exec()
        #   warning: do not use `sys.exit(self.exec())`, because
        #   `self.__hidden_ref` will be released before qml triggered
        #   `Component.onDestroyed`. then there will be an error 'cannot call
        #   from null!'
    
    # alias for compatible.
    #   https://ux.stackexchange.com/questions/106001/do-we-open-or-launch-or
    #   -startapps+&cd=1&hl=zh-CN&ct=clnk&gl=sg
    launch = start = open = run
    
    def show_splash_screen(self, file: str) -> None:
        assert exists(file)
        
        from qtpy.QtCore import Qt
        from qtpy.QtGui import QPixmap
        from qtpy.QtWidgets import QSplashScreen, QWidget
        
        pixmap = QPixmap(file)  # noqa
        splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
        splash.setMask(pixmap.mask())
        
        def on_close():
            nonlocal splash
            print(':v', 'close splash screen')
            splash.hide()
            splash.finish(QWidget())  # noqa
        
        self.engine.objectCreated.connect(on_close)  # noqa
        
        splash.show()
        self.processEvents()
    
    # -------------------------------------------------------------------------
    
    def on_exit_register(self, func: t.Callable) -> int:
        self._on_exit_funcs.append(func)
        return len(self._on_exit_funcs) - 1
    
    def _exit(self) -> None:
        """
        dev note:
            must release `self.engine` first, then `self._register.__hidden_ref`.
            if not so, the deading app will report all hidden refs are losing,
            which is actually an expected behavior (we do not need the reports).
        
        ref:
            search keywords: 'QML TypeError: Cannot read property of null'
            link: https://bugreports.qt.io/browse/QTBUG-81247?focusedCommentId
                =512347&page=com.atlassian.jira.plugin.system.issuetabpanels
                :comment-tabpanel#comment-512347
        """
        for f in self._on_exit_funcs:
            try:
                f()
            except Exception as e:
                print(':v4', 'error on app exit', f, e)
                continue
        self._on_exit_funcs.clear()
        print('[red dim]exit application[/]', ':r')
        del self.engine
        self._register.release()


app = Application()
