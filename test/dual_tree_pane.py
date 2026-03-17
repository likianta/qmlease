import os
import qmlease as qe
from argsense import cli
from lk_utils import fs

class Main(qe.QObject):
    
    def __init__(self, exmaple_folder):
        super().__init__()
        self._root = fs.normpath(exmaple_folder)
    
    @qe.Slot(object, object)
    def init_ui(self, left_tree, right_tree):
        left_tree['model'] = m0 = self._init_left_tree_model()
        right_tree['model'] = m1 = qe.Model(
            ('type', 'name', 'path', 'children')
        )

        _checked_paths = set()
        _unchecked_paths = set()

        @qe.bind_signal(left_tree.nodeChecked)
        def _(path: str, checked: bool) -> None:
            print(path, checked)

            if path == self._root:
                _checked_paths.clear()
                _unchecked_paths.clear()
                if checked:
                    _checked_paths.add(path)
                    m1.clear()
                    m1.append(m0[0])
                return
            
            if checked:
                for x in tuple(_checked_paths):
                    if x.startswith(path + '/'):
                        _checked_paths.remove(x)
                for x in tuple(_unchecked_paths):
                    if x.startswith(path + '/'):
                        _unchecked_paths.remove(x)
                _checked_paths.add(path)
            else:
                if path in _checked_paths:
                    _checked_paths.remove(path)
                else:
                    for x in tuple(_checked_paths):
                        if x.startswith(path + '/'):
                            _checked_paths.remove(x)
                    for x in tuple(_unchecked_paths):
                        if x.startswith(path + '/'):
                            _unchecked_paths.remove(x)
                    _unchecked_paths.add(path)
            _recalculate_model()

        def _recalculate_model():
            common_root = fs.normpath(os.path.commonpath(_checked_paths))
            print(common_root)
            # m0 = window['model0']
            # m1 = window['model1']
            m1.clear()
            m1.append({
                'type'    : 'folder',
                'name'    : fs.basename(common_root),
                'path'    : common_root,
                'children': qe.Model(('type', 'name', 'path', 'children')),
            })

            def path_to_node(path):
                return _recurse_find_node_from_m0(m0, path)

            def add_node_to_m1(node):
                _recurse_add_node(m1, node)

            def _recurse_find_node_from_m0(node_list, target_path):
                for node in node_list:
                    if node['path'] == target_path:
                        if node['type'] == 'file':
                            return node
                        else:
                            for x in sorted(_unchecked_paths):
                                if x.startswith(node['path'] + '/'):
                                    return {
                                        'type'    : node['type'],
                                        'name'    : node['name'],
                                        'path'    : node['path'],
                                        'children': qe.Model.from_list(list(
                                            _pick_out_unchecked_nodes(
                                               node['children'], x
                                            )
                                        )),
                                    }
                            else:
                                return node
                    elif target_path.startswith(node['path'] + '/'):
                        return _recurse_find_node_from_m0(
                            node['children'], target_path
                        )
                raise Exception('path not found: {}'.format(target_path))

            def _pick_out_unchecked_nodes(xlist, del_path):
                for node in xlist:
                    if node['path'] == del_path:
                        return
                    elif del_path.startswith(node['path'] + '/'):
                        yield {
                            'type'    : node['type'],
                            'name'    : node['name'],
                            'path'    : node['path'],
                            'children': qe.Model.from_list(list(
                                _pick_out_unchecked_nodes(
                                    node['children'], del_path
                                )
                            )),
                        }
                    else:
                        yield node

            def _recurse_add_node(node_list, target_node, _from_path=''):
                parent_path = fs.parent(target_node['path'])
                for node in node_list:
                    if node['path'] == target_node['path']:
                        # print(
                        #     target_node, 
                        #     target_node['path'], 
                        #     target_node['children'], 
                        #     ':vl'
                        # )
                        node['children'].append_many(target_node['children'])
                        return
                    elif node['path'] == parent_path:
                        node['children'].append(target_node)
                        return
                    elif parent_path.startswith(node['path'] + '/'):
                        _recurse_add_node(
                            node['children'], target_node, node['path']
                        )
                        return
                else:
                    assert _from_path
                    temp_list = node_list
                    temp_path = _from_path
                    for part in parent_path.split('/'):
                        temp_path += '/' + part
                        temp_list.append({
                            'type'    : 'folder',
                            'name'    : part,
                            'path'    : temp_path,
                            'children': qe.Model(
                                ('type', 'name', 'path', 'children'), 
                                autocomplete=False
                            ),
                        })
                        temp_list = temp_list[-1]['children']
                    temp_list.append(target_node)

            for path in sorted(_checked_paths):
                print(path, ':i')
                add_node_to_m1(path_to_node(path))

        # def _remoev_existing_subnode_from_model(del_path):
        #     def recurse_remove(xlist, target_path):
        #         for i, node in enumerate(xlist):
        #             if node['path'] == target_path:
        #                 xlist.delete(i)
        #                 return
        #             elif target_path.startswith(node['path'] + '/'):
        #                 recurse_remove(node['children'], target_path)
        #                 return
        #         else:
        #             raise Exception('path not found: {}'.format(target_path))
        #     recurse_remove(m1, del_path)
    
    def _init_left_tree_model(self):
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
