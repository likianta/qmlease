import typing as t

from lk_utils import load
from qtpy.QtWidgets import QApplication

from .base import Base
from .base import T
from .._env import IS_WINDOWS


class Font(Base):
    
    def update_from_file(self, file: str) -> None:
        data: dict = load(file)
        if not data.get('font_default'):
            if IS_WINDOWS:
                data['font_default'] = self._search_font(
                    'Microsoft YaHei UI', strict=True
                )
            else:
                data['font_default'] = QApplication.font().family()
        if not data.get('font_monospaced'):
            if IS_WINDOWS:
                data['font_monospaced'] = self._search_font(
                    'Cascadia Code', 'Consolas', 'Courier New', strict=True
                )
            else:
                data['font_monospaced'] = 'DejaVu Sans Mono'
                #   candidates: Monospace, Ubuntu Mono, etc.
        # data['font_monospaced_with_fallback'] = '"{}","{}"'.format(
        #     data['font_monospaced'], data['font_default']
        # )
        self.update(data)
    
    def _normalize(self, data: T.Data) -> T.Data:
        return data
    
    def _create_similars(self, data: T.Data) -> T.Data:
        return data
    
    def _shortify(self, data: T.Data) -> T.Data:
        for k, v in data:
            if k.endswith('_default'):
                yield k[:-8], v
            elif k.endswith('_m'):
                yield k[:-2], v
            elif k.endswith('_monospaced'):
                yield k[:-1], v
                yield k[:-6], v
            # elif 'monospaced' in k:
            #     yield k.replace('monospaced', 'mono'), v
            #     yield k.replace('monospaced', 'monospace'), v
    
    def _search_font(
        self, *candidates: str, strict: bool = False
    ) -> t.Optional[str]:
        """
        depend on different OS:
            linux: use `fc-list`.
            windows: search in `C:/Windows/Fonts/`.
                or: https://stackoverflow.com/a/75783992/9695911
            macos: fonts are in `/Library/Fonts/` or `~/Library/Fonts/`.
        """
        if IS_WINDOWS:
            import winreg
            reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            key = winreg.OpenKey(
                reg,
                r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts',
                0,
                winreg.KEY_READ
            )
            families = set()
            for i in range(0, winreg.QueryInfoKey(key)[1]):
                # e.g. winreg.EnumValue(key, i)
                #   -> ('Consolas Bold (TrueType)', 'consolab.ttf', 1)
                font_name = winreg.EnumValue(key, i)[0]
                font_name = (
                    font_name
                    .replace('(TrueType)', '')
                    .replace('(All res)', '')
                    .strip()
                )
                if ' & ' in font_name:
                    # e.g. 'Microsoft YaHei & Microsoft YaHei UI'
                    families.update(font_name.split(' & '))
                else:
                    families.add(font_name)
                
            for x in candidates:
                if x in families:
                    return x
            else:
                if strict:
                    # raise Exception(sorted(candidates), sorted(families))
                    print(':lv8', sorted(candidates), sorted(families))
                    raise Exception
        else:
            raise NotImplementedError
