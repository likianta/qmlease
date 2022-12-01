from os import listdir

from .base import ResourceManager


class AssetsResourceManager(ResourceManager):
    from lk_utils import relpath
    assets_dir = relpath('../../themes/Theme/Assets')
    icons_dir = f'{assets_dir}/icons'
    index: dict
    
    def __init__(self):
        super().__init__(None)
        self._indexing_assets()
    
    def _indexing_assets(self):
        self.index = {}
        for d in listdir(self.assets_dir):
            for n in listdir(f'{self.assets_dir}/{d}'):
                self.index[n] = f'{self.assets_dir}/{d}/{n}'
    
    def _get(self, name, **kwargs):
        return f'file:///{self.index[name]}'
