from ._base import Base


class Font(Base):
    def _get_abbrs(self, name: str):
        if name.endswith('_m'):
            yield name[:-2]
        elif name.endswith('_default'):
            yield name[:-8]
    
    def update_from_file(self, file: str):
        from lk_utils import loads
        data: dict = loads(file)
        
        if 'font_default' in data:
            if data['font_default'] == '':
                from qtpy.QtWidgets import QApplication
                from os import name
                if name == 'nt':
                    font = 'Microsoft YaHei UI'
                else:
                    font = QApplication.font().family()  # noqa
                data['font_default'] = font
        
        self.update(data)
