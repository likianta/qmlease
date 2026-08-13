import qmlease as qe


class SideBar(qe.QObject):
    @qe.Slot(result=list)
    def init_model(self):
        model = qe.ListModel.from_list(
            fields=('text', 'icon'),
            data=(
                (
                    'Dashboard',
                    qe.pyassets.cwd('examples/')
                )
            )
        )
        model = qe.ListModel(('text', 'icon'))
        model.extend()
