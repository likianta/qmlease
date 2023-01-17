import typing as t

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
    @slot(dict, result=str)
    @slot(str, str, result=str)
    def file_dialog(
            self,
            action='open',
            type_='file',
            type_filter: t.Union[dict, str, None] = None,
            start_dir='',
            title='',
            backend='qt',
            use_native_dialog=True
    ) -> str:
        """
        args:
            action: literal['open', 'save']
            type_: literal['file', 'folder']
            type_filter:
                dict: dict[str label, list_or_tuple patterns]
                    e.g.
                        {'Image': ['*.png', '*.jpg']}
                        {'Text': ['*.txt', '*.md'], 'Image': ['*.png', '*.jpg'],
                         'All': ['*']}
                str: see QFileDialog.
            start_dir:
                if not specified, will do the default behavior (remembering
                last selected path).
                use '.' to always open current working dir.
            backend: literal['qt', 'tk']
                warning: use 'tk' cannot remember last opened folder.
            use_native_dialog: bool. deprecated!
                set to False may resolve some issue that cannot remember the
                last opened directory (it's a rare case).
        """
        if isinstance(action, dict):  # this is a workaround for qml call.
            kwargs = action
            return self.file_dialog(**kwargs)
        
        if not title:
            title = '{do} a {thing}'.format(
                do='Open' if action == 'open' else 'Save',
                thing='File' if type_ == 'file' else 'Folder'
            )
        # check start_dir
        if start_dir:
            from os import path as ospath
            if not ospath.exists(start_dir) or ospath.isfile(start_dir):
                start_dir = ospath.dirname(start_dir)
            if not ospath.isdir(start_dir):
                print(':v3', 'invalid start direcotry, will fallback to '
                             'default behavior', start_dir)
                start_dir = ''
        # make sure type_filter finally be a string or null stuff.
        if type_filter:
            if isinstance(type_filter, dict):
                if backend == 'qt':
                    type_filter = ';;'.join(
                        '{label} ({patterns})'.format(
                            label=label,
                            patterns=' '.join(patterns)
                        ) for label, patterns in type_filter.items()
                    )
                else:
                    type_filter = ' '.join(
                        ' '.join(patterns) for patterns in type_filter.values()
                    )
        else:
            if backend == 'qt':
                type_filter = ...
            else:
                type_filter = None
        
        if backend == 'qt':
            from qtpy.QtWidgets import QFileDialog
            kwargs = {
                'parent' : None,
                'caption': title,
                'dir'    : start_dir,
                'filter' : type_filter,
            }
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
                    raise ValueError('Cannot save folder!')
        else:
            from tkinter import Tk
            from tkinter import filedialog
            root = Tk()
            root.withdraw()
            kwargs = {
                'title'     : title,
                'initialdir': start_dir or None,
                'filetypes' : type_filter,
            }
            if action == 'open':
                if type_ == 'file':
                    return filedialog.askopenfilename(**kwargs)
                else:
                    return filedialog.askdirectory(**kwargs)
            else:
                if type_ == 'file':
                    return filedialog.asksaveasfilename(**kwargs)
                else:
                    raise ValueError('Cannot save folder!')


util = Util()
