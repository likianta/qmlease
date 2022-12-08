from lk_utils import loads

from ._base import Base


class Font(Base):
    
    def _post_complete(self, data: dict) -> dict:
        for k, v in tuple(data.items()):
            if '_' in k:
                if k.endswith('_m'):
                    data[k[:-2]] = v
                elif not k.endswith(('_xxs', '_xs', '_s', '_l', '_xl', '_xxl')):
                    data[f'{k}_m'] = v
            else:
                data[f'{k}_m'] = v
        return data
    
    def update_from_file(self, file: str):
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
