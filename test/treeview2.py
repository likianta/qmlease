import qmlease as qe
from lk_utils import fs

class TreeView(qe.QObject):
    @qe.Slot(object)
    def init_ui(self, window):
        @qe.bind_signal(window.pathSubmit)
        def _(path: str):
            print(path, ':v2')
            assert fs.isdir(path)

            def recurse(folder) -> qe.Model:
                children = []
                for d in fs.find_dirs(folder):
                    children.append({
                        'type': 'folder',
                        'name': d.name,
                        'path': d.path,
                        'children': recurse(d.path),
                    })
                for f in fs.find_files(folder):
                    children.append({
                        'type': 'file',
                        'name': f.name,
                        'path': f.path,
                    })
                return qe.Model.from_list(children)

            model = [
                {
                    'type': 'folder',
                    'name': fs.basename(path),
                    'path': fs.normpath(path),
                    'children': recurse(path),
                }
            ]
            # window['model'] = model
            window['model'] = qe.Model.from_list(model)

qe.app.register(TreeView(), 'main')
qe.app.run(fs.xpath('treeview2.qml'))
