from qtpy.QtCore import QObject

from ...qtcore import slot

H_LEFT = 1
H_CENTER = 4
H_RIGHT = 2
V_TOP = 32
V_CENTER = 128
V_BOTTOM = 64


class ContentAlignment:
    
    @slot(object, str)
    def quick_align(self, qobj: QObject, alignment: str):
        def _normalize_alignment(alignment: str):
            for k, v in {
                'hcenter': (H_CENTER, V_TOP),
                'vcenter': (H_LEFT, V_CENTER),
                'center' : (H_CENTER, V_CENTER),
            }.items():
                if alignment == k:
                    return v
            
            # noinspection PyUnusedLocal
            final_h = final_v = None
            
            for k, v in {
                # respect `dict.keys` order, i.e. check word first, check its
                # initial letter second.
                'left' : H_LEFT,
                'l'    : H_LEFT,
                'right': H_RIGHT,
                'r'    : H_RIGHT,
            }.items():
                if alignment.startswith(k):
                    final_h = v
                    alignment = alignment.replace(k, '', 1)
                    break
            
            alignment = alignment.lstrip('-')
            
            for k, v in {
                'top'   : V_TOP,
                't'     : V_TOP,
                'bottom': V_BOTTOM,
                'b'     : V_BOTTOM,
                'center': V_CENTER,
            }.items():
                if alignment.startswith(k):
                    final_v = v
                    return final_h, final_v
            
            raise Exception('Illegal alignment', alignment)
        
        h, v = _normalize_alignment(alignment)
        qobj.setProperty('horizontalAlignment', h)
        qobj.setProperty('verticalAlignment', v)
