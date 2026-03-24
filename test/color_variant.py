import qmlease as qe
from functools import partial
from materialyoucolor.contrast import Contrast
from materialyoucolor.hct import Hct

class Main(qe.QObject):

    @qe.Slot(object)
    def init_ui(self, root):
        self._root = root

        def _update_ratio(hex0, hex1):
            hct0 = Hct.from_int(hex_to_argb(hex0))
            hct1 = Hct.from_int(hex_to_argb(hex1))
            root['ratio'] = round(
                Contrast.ratio_of_tones(hct1.tone, hct0.tone), 2
            )

        root.colorPairChanged.connect(_update_ratio)
        # root.requestContainerColorLight.connect(
        #     partial(self.make_container_color, light=True)
        # )
        # root.requestContainerColorDark.connect(
        #     partial(self.make_container_color, light=False)
        # )

    @qe.Slot(str)
    @qe.Slot(str, bool)
    def make_container_color(self, fg: str, light: bool = True):
        hct1 = Hct.from_int(hex_to_argb(fg))
        hct0 = Hct.from_hct(hct1.hue, hct1.chroma, 90 if light else 40)
        hex0 = argb_to_hex(hct0.to_int())
        self._root['rectColor0'] = hex0
        self._root.colorPairChanged.emit(hex0, fg)
    
def argb_to_hex(argb: int) -> str:
    # print(hex(argb), ':pv')
    return f'#{argb & 0xFFFFFF:06x}'

def hex_to_argb(value: str) -> int:
    return 0xFF << 24 | int(value[1:], 16)

def hex_to_rgb(hex):
    pass

qe.app.register(Main())
qe.app.run('test/color_variant.qml')
