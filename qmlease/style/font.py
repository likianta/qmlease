import typing as t

from lk_utils import load
from qtpy.QtWidgets import QApplication

from .size import Size
from .._env import IS_WINDOWS


class Font(Size):
    
    def update_from_file(self, file: str) -> None:
        data: dict = load(file)
        if 'font_default' not in data:
            if IS_WINDOWS:
                data['font_default'] = self._search_font(
                    'Microsoft YaHei UI', strict=True
                )
            else:
                data['font_default'] = QApplication.font().family()
        if 'font_monospace' not in data:
            if IS_WINDOWS:
                data['font_monospaced'] = self._search_font(
                    'Cascadia Code', 'Consolas', 'Courier New', strict=True
                )
            else:
                data['font_monospaced'] = 'DejaVu Sans Mono'
                #   candidates: Monospace, Ubuntu Mono, etc.
        self.update(data)

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
    
    def _shortify(self, data: dict) -> dict:
        out = {}
        for k, v in data.items():
            if k.endswith('_m'):
                out[k[:-2]] = v
            elif k.endswith('monospaced'):
                out[k[:-1]] = v
                out[k[:-6]] = v
        return out
