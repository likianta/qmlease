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
    @slot(str, str, str, str, result=str)
    @slot(str, str, str, str, bool, result=str)
    def file_dialog(
            self,
            action='open',
            type_='file',
            title='Confirm file selection',
            backend='qt',
            use_native_dialog=True
    ) -> str:
        """
        args:
            action: literal['open', 'save']
            type_: literal['file', 'folder']
            backend: literal['qt', 'tk']
                warning: use 'tk' cannot remember last opened folder.
            use_native_dialog: bool. deprecated!
                set to False may resolve some issue that cannot remember the
                last opened directory (it's a rare case).
        
        tip:
            params are too many. you can use `pyside.kwcall` to bypass the slot
            limitation:
                // example.qml
                const path = pyside.kwcall(
                    lkutil, 'file_dialog', {
                        action: 'open',
                        type_: 'folder',
                    }
                )
        """
        if backend == 'qt':
            from qtpy.QtWidgets import QFileDialog
            kwargs = {'parent': None, 'caption': title, 'dir': ''}
            if not use_native_dialog:
                # noinspection PyUnresolvedReferences
                kwargs['options'] = QFileDialog.DontUseNativeDialog
            if action == 'open':
                if type_ == 'file':
                    return QFileDialog.getOpenFileName(**kwargs)[0]
                else:
                    return QFileDialog.getExistingDirectory(**kwargs)
            else:
                if type_ == 'file':
                    return QFileDialog.getSaveFileName(**kwargs)[0]
                else:
                    raise ValueError('Cannot save folder.')
        else:
            from tkinter import Tk
            from tkinter import filedialog
            root = Tk()
            root.withdraw()
            if action == 'open':
                if type_ == 'file':
                    return filedialog.askopenfilename(title=title)
                else:
                    return filedialog.askdirectory(title=title)
            else:
                if type_ == 'file':
                    return filedialog.asksaveasfilename(title=title)
                else:
                    raise ValueError('Cannot save folder.')


util = Util()
