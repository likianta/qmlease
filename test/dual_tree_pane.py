import qmlease as qe
from argsense import cli
from lk_utils import fs

class Main(qe.QObject):
    
    def __init__(self, exmaple_folder):
        super().__init__()
        self._root = fs.normpath(exmaple_folder)
    
    @qe.Slot(object, object)
    def init_ui(self, source_tree, target_tree):
        source_tree['model'] = self._init_source_tree_model()
        # target_tree['model'] = qe.Model(
        #     ('type', 'name', 'path', 'children')
        # )

        @qe.bind_signal(source_tree.nodeChecked)
        def _(path: str, checked: bool) -> None:
            print(path, checked)
            target_tree['model'] = source_tree.extractCheckedTree()

    def _init_source_tree_model(self):
        def recurse(folder):
            children = []
            for d in fs.find_dirs(folder):
                print(fs.relpath(d.path, self._root), ':vi')
                children.append({
                    'type'    : 'folder',
                    'name'    : d.name,
                    'path'    : d.path,
                    'children': recurse(d.path),
                })
            for f in fs.find_files(folder):
                children.append({
                    'type'   : 'file',
                    'name'   : f.name,
                    'path'   : f.path,
                })
            return qe.Model.from_list(children)
        
        return qe.Model.from_list(
            [
                {
                    'type'    : 'folder',
                    'name'    : fs.basename(self._root),
                    'path'    : self._root,
                    'children': recurse(self._root),
                }
            ]
        )

@cli
def main(example_folder):
    qe.app.register(Main(example_folder))
    qe.app.run(fs.xpath('dual_tree_pane.qml'))


if __name__ == '__main__':
    cli.run(main)
