import qmlease as qe
from lk_utils import fs


class Sidebar(qe.QObject):
    @qe.Slot(result=qe.ListModel)
    def init_model(self) -> qe.ListModel:
        self._model = qe.ListModel.from_list(
            # ^^^^^ we must hold the reference of the model to prevent python GC.
            fields=('text', 'icon'),
            data=(
                ('Dashboard', qe.pyassets.here('readiness_score.svg')),
                ('Power Management', qe.pyassets.here('flashlight_fill.svg')),
                ('Chipboard', qe.pyassets.here('cpu_line.svg')),
            ),
        )
        return self._model


qe.app.set_font_family('Cascadia Code')
qe.app.register(Sidebar())
qe.app.run(fs.here('sidebar.qml'))
