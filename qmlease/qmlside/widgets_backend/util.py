from .__ext__ import QObject
from .__ext__ import slot


class Util(QObject):
    
    @slot(result=str)
    def get_monospaced_font(self) -> str:
        """ get an available monospaced font family name based on OS. """
        from platform import system
        name = system()
        if name == 'Darwin':
            return 'Menlo'
        elif name == 'Windows':
            return 'Consolas'
        else:
            return 'Ubuntu Mono'
    
    @slot(result=str)
    @slot(str, result=str)
    @slot(str, str, result=str)
    @slot(str, str, str, result=str)
    def open_file_dialog(
            self, action='open', title='Confirm file selection', opener='qt',
    ) -> str:
        """
        args:
            action: literal['open', 'save']
            opener: literal['auto', 'tk', 'qt']
        """
        if (opener == 'auto' and _has_tkinter()) or opener == 'tk':
            from tkinter import Tk
            root = Tk()
            root.withdraw()
            if action == 'open':
                from tkinter.filedialog import askopenfilename
                return askopenfilename(title=title)
            else:
                from tkinter.filedialog import asksaveasfilename
                return asksaveasfilename(title=title)
        else:  # _opener == 'qt'
            from qtpy.QtWidgets import QFileDialog
            dialog = QFileDialog(None)
            if action == 'open':
                return dialog.getOpenFileName(caption=title)[0]
            else:
                return dialog.getSaveFileName(caption=title)[0]


def _has_tkinter() -> bool:
    try:
        import tkinter
        return True
    except ImportError:
        return False


util = Util()
