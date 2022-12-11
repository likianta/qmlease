import os

from lk_utils import fs
from lk_utils import loads

dist_dir = fs.xpath('../dist')


def tailor(dir_i: str, scheme='alpha-0') -> None:
    """
    args:
        dir_i: a path to "PySide6" directory. it must be under "dist" folder.
            make sure "dist/deleted" folder is not existed.
    
    kwargs:
        scheme (-s): check `pptailor/deletable_list.yaml` for details.
    """
    dir_i = fs.normpath(dir_i)
    assert dir_i.endswith('dist/pyside6_lite/PySide6')
    
    dir_o = dir_i  # the same dir
    dir_x = f'{dist_dir}/deleted'
    assert not os.path.exists(dir_x)
    os.mkdir(dir_x)
    
    size_i: str = _get_folder_size(dir_i)
    size_o: str
    
    deletable_paths = loads(fs.xpath('deletable_list.yaml'))[scheme]
    
    for p in deletable_paths:
        print('delete', p, ':iv4s')
        move_i = f'{dir_i}/{p}'
        move_o = f'{dir_x}/{p.replace("/", "--")}'
        fs.move(move_i, move_o)
    
    size_o = _get_folder_size(dir_o)
    print('the size is tailored from '
          '[red]{}[/] to [green]{}[/]'.format(size_i, size_o), ':rv2')
    print(f'see produced result at {dir_o}')


def restore(dir_i: str) -> None:
    dir_o = dir_i
    dir_x = f'{dist_dir}/deleted'
    assert os.path.exists(dir_x)
    for p in os.listdir(dir_x):
        print('restore', p)
        move_i = f'{dir_x}/{p}'
        move_o = f'{dir_o}/{p.replace("--", "/")}'
        fs.move(move_i, move_o)
    fs.remove_tree(dir_x)


def _get_folder_size(folder: str) -> str:
    # the size unit should be 'MB'
    size = sum(os.path.getsize(x) for x in fs.findall_file_paths(folder))
    return f'{size / 1024 / 1024:.2f} MB'
