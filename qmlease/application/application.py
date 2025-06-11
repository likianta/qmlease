import os
import typing as t

from lk_utils import fs
from qtpy.QtGui import QIcon
from qtpy.QtQml import QQmlApplicationEngine
from qtpy.QtQml import QQmlContext
from qtpy.QtWidgets import QApplication

from .register import Register
from .._env import IS_WINDOWS
from .._env import QT_API
from ..qtcore import signal


class Application(QApplication):
    engine: QQmlApplicationEngine
    root: QQmlContext
    on_exit: signal
    _on_exit_funcs: t.List[t.Callable]
    _register: Register
    
    def __init__(self, app_name: str = 'QmlEase', **kwargs) -> None:
        """
        params:
            app_name: str
                set application name.
                the name can also be changed by calling `self.set_app_name`.
            kwargs:
                organization: str. default 'dev.likianta.qmlease'
                    set an organization name, this avoids an error from \
                    `QtQuick.Dialogs.FileDialog`.
        """
        # setup debug config for qmljs
        # ref: https://marketplace.visualstudio.com/items?itemName=orcun \
        # -gokbulut.qml-debug
        if x := os.getenv('QMLEASE_DEBUG_JS'):
            # the `x` can either be '1' or a series of comma-separated \
            # options e.g. 'host:127.0.0.1,port:1234,block,services \
            # :DebugMessages'. if '1' is given, will use default options.
            if x == '1':
                options = ('host:127.0.0.1,port:12150,block,services'
                           ':DebugMessages,QmlDebugger,V8Debugger')
            else:
                assert 'host' in x and 'port' in x, ('insufficient options', x)
                options = x
            qargs = f'-qmljsdebugger={options}'
            print(qargs, ':vs')
            super().__init__([app_name, qargs])  # noqa
        else:
            super().__init__()
        
        self.setApplicationName(app_name)
        self.setOrganizationName(kwargs.get(
            'organization', 'dev.likianta.qmlease'
        ))
        
        self.engine = QQmlApplicationEngine()  # noqa
        self.root = self.engine.rootContext()
        self._on_exit_funcs = []
        self._register = Register(self.root)
        
        self.register = self._register.register
        
        self._ui_fine_tune()
        self.register_qmldir(fs.xpath('../widgets'))
        self.on_exit = super().aboutToQuit  # noqa
    
    def _ui_fine_tune(self) -> None:
        if IS_WINDOWS:
            self.setFont('Microsoft YaHei UI')  # noqa
    
    # -------------------------------------------------------------------------
    
    def set_app_name(self, name: str) -> None:
        # just made a consistent snake-case function alias for external caller,
        # especially for who imports a global instance `app` from this module.
        self.setApplicationName(name)
    
    def set_app_icon(self, file: str) -> None:
        self.setWindowIcon(QIcon(file))  # noqa
    
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
                '*.qml' files. see example of '../widgets'.
        """
        if not fs.exist(qmldir):
            print(':v3p', 'the qmldir not exists! it may cause a "xxx is not '
                          'installed" error in qml side.', qmldir)
        self.engine.addImportPath(qmldir)
    
    def _register_backend(self) -> None:
        from ..pyside import pyside
        from ..qmlside import pyassets, pybroad, pylayout  # DELETE
        from ..qmlside import widgets_backend as wb  # DELETE
        from ..qmlside.widgets_backend import WidgetBackend
        from ..style import pyenum, pystyle
        
        self.register(WidgetBackend(), 'widget', 'qmlease', verbose=False)
        
        self.register(pyassets, 'pyassets', 'global', verbose=False)
        self.register(pybroad, 'pybroad', 'global', verbose=False)
        self.register(pyenum, 'pyenum', 'global', verbose=False)
        self.register(pylayout, 'pylayout', 'global', verbose=False)
        self.register(pyside, 'pyside', 'global', verbose=False)
        self.register(pystyle, 'pystyle', 'global', verbose=False)
        self.register(pystyle.color, 'pycolor', 'global', verbose=False)
        self.register(pystyle.font, 'pyfont', 'global', verbose=False)
        self.register(pystyle.motion, 'pymotion', 'global', verbose=False)
        self.register(pystyle.size, 'pysize', 'global', verbose=False)
        
        self.register(wb.ListView(), 'lklistview', 'global', verbose=False)
        self.register(wb.Progress(), 'lkprogress', 'global', verbose=False)
        self.register(wb.ScopeEngine(), 'lkscope', 'global', verbose=False)
        self.register(wb.Slider(), 'lkslider', 'global', verbose=False)
        self.register(wb.logger, 'lklogger', 'global', verbose=False)
        self.register(wb.util, 'lkutil', 'global', verbose=False)
        
        pyassets.add_source(fs.xpath('../widgets/LKWidgets'), 'lkwidgets')
    
    # -------------------------------------------------------------------------
    
    def run(self, qmlfile: str, debug: bool = False) -> None:
        self._register.freeze()
        if debug:
            from ..qmlside import HotReloader
            reloader = HotReloader(app, qmlfile)
            reloader.run()
        else:
            self._run(qmlfile)
    
    def _run(self, qmlfile: str) -> None:
        """
        note: do not merge this method into `run`, because -
        `..qmlside.HotReloader` internally uses this.
        """
        self._register_backend()
        self.engine.load('file:///' + fs.abspath(qmlfile))
        self.on_exit.connect(self._exit)
        if QT_API in ('pyside2', 'pyqt5'):
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
        assert fs.exist(file)
        
        from qtpy.QtCore import Qt
        from qtpy.QtGui import QPixmap
        from qtpy.QtWidgets import QSplashScreen, QWidget
        
        pixmap = QPixmap(file)  # noqa
        splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)  # noqa
        splash.setMask(pixmap.mask())
        
        def on_close() -> None:
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
        self.engine = QQmlApplicationEngine()  # noqa
        self._register.release()


if _inst := QApplication.instance():
    # workaround
    #   when qmlease is mixed using with streamlit framework, for example the -
    #   developer wants both a native ui and web ui for different purposes. -
    #   this workaround helps to avoid streamlit rerun crashed by QApplication -
    #   singleton.
    # original error message:
    #   RuntimeError: Please destroy the Application singleton before creating -
    #   a new Application instance.
    # related links:
    #   https://stackoverflow.com/questions/53387733/how-to-get-the-current -
    #   -qapplication
    # print(
    #     _inst,
    #     _inst.__class__,  # <class 'qmlease.application.application.Application'>
    #     _inst.__class__.__qualname__,  # 'Application'
    #     _inst.__module__,  # 'qmlease.application.application'
    #     isinstance(_inst, Application),  # False (why?)
    #     isinstance(_inst, QApplication),  # True
    #     ':vl'
    # )
    # assert _inst.__class__ is Application
    assert _inst.__module__ == 'qmlease.application.application'
    app = _inst
else:
    app = Application()
