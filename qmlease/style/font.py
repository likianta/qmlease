from lk_utils import loads

from .size import Size


class Font(Size):
    
    def update_from_file(self, file: str):
        data: dict = loads(file)
        if 'font_default' in data:
            if data['font_default'] in ('', 'default', 'system', '$system'):
                from os import name
                from qtpy.QtWidgets import QApplication
                if name == 'nt':
                    font = 'Microsoft YaHei UI'
                else:
                    font = QApplication.font().family()  # noqa
                data['font_default'] = font
        self.update(data)
