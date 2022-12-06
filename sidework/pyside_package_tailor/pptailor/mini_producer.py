import os

from lk_utils import fs
from lk_utils import loads


def main(dir_i: str, dir_o: str, scheme='alpha-0') -> None:
    """
    produce a subset of pyside6 package.
    [green](this method uses `os.symlink` to generate copies. it is very fast -
    and safe.)[/]
    
    args:
        dir_i: a path to "PySide6" directory.
        dir_o: give a directory path, will generate "PySide6" under it.
            if "PySide6" already exists in it, will:
                - if it is an empty directory, will delete and recreate it.
                - if it is an old result, will delete and recreate it.
                - else, will raise FileExistsError.
    
    kwargs:
        scheme (-s): check `pptailor/deletable_list.yaml` for more details.
    """
    assert dir_i.endswith('PySide6')
    assert not dir_o.endswith('PySide6')
    dir_o += '/PySide6'
    
    index_i = fs.xpath('deletable_list.yaml')
    index_o = f'{dir_o}/deletable_list.yaml'
    
    path_list = loads(index_i)[scheme]
    
    # check dir_o
    if os.path.exists(dir_o):
        if os.path.exists(index_o):
            fs.remove_tree(dir_o)
        elif os.listdir(dir_o):
            raise FileExistsError(f'"{dir_o}" is not empty')
    fs.make_dir(dir_o)
    fs.copy_file(index_i, index_o, True)
    
    # link files
    for d in sorted(set(x for x in path_list if x.endswith('/'))):
        fs.make_dirs(f'{dir_o}/{d}')
    
    for p in path_list:
        print(f'linking {p}', ':i')
        fs.make_link(f'{dir_i}/{p}', f'{dir_o}/{p}')
        
    print('the size is tailored from [red]{}[/] to [green]{}[/]'.format(
        _get_folder_size(dir_i), _get_folder_size(dir_o)
    ), ':rv2')
    print(f'see produced result at {dir_o}')
    print('you may test it by `py -m pptailor test-package ...` and it works, '
          'you can compress it to be a ".zip" file.')


def _get_folder_size(folder: str) -> str:
    # the size unit should be 'MB'
    size = sum(os.path.getsize(x) for x in fs.findall_file_paths(folder))
    return f'{size / 1024 / 1024:.2f} MB'
