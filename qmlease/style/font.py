from lk_utils import load
from qtpy.QtWidgets import QApplication

from .size import Size
from .._env import IS_WINDOWS


class Font(Size):
    
    def update_from_file(self, file: str):
        data: dict = load(file)
        if 'font_default' in data:
            if data['font_default'] in ('', 'default', 'system', '$system'):
                if IS_WINDOWS:
                    font = 'Microsoft YaHei UI'
                else:
                    font = QApplication.font().family()  # noqa
                data['font_default'] = font
        self.update(data)
