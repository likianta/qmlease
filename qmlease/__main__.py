"""
usage:
    run in command line:
        py -m qmlease -h
        py -m qmlease run <qml_file>
        py -m qmlease run <qml_file> --debug
        ...
"""
from argsense import cli


@cli
def run(qml_file: str, debug: bool = False, **kwargs) -> None:
    """
    run target QML file.
    
    params:
        debug (-d): enable hot reload.
        **kwargs:
            window_size (-s): e.g. "800x600"
            print_with_varnames (-v): bool
    """
    from .application import app
    if x := kwargs.get('window_size'):
        w, h = map(int, x.split('x'))
        kwargs['window_size'] = (w, h)
    app.run(qml_file, debug=debug, **kwargs)


@cli
def list_builtin_pyhandlers() -> None:
    """
    List global registered pyhandler names which are available across all -
    QML files.
    
    Example usage:
        [dim]// view.qml[/]
        [dim]// assume `pyside` and `pylayout` are built-in pyhandlers.[/]
        [red]import[/] [magenta]QtQuick[/]
        [yellow]Column[/] {
            [green]width[/]: [cyan][b]pyside[/].call('get_init_width')[/]
            [dim]//     ^^^^^^[/]
            [green]height[/]: [cyan][b]pyside[/].call('get_init_height')[/]
            [dim]//      ^^^^^^[/]
            [yellow]Component.[i]onCompleted[/][/]: {
                [cyan][b]pylayout[/].auto_align(this, 'hcenter,hfill')[/]
            [dim]//  ^^^^^^^^[/]
            }
        }
    """
    print(
        '''
        - pyside
        - pystyle
            - pycolor
            - pyfont
            - pymotion
            - pysize
        - pyalign
        - pycolor
        - pyfont
        - pymotion
        - pysize
        - pylayout
        - pyrss
        ''',
        ':r2'
    )


if __name__ == '__main__':
    # pox -m qmlease run unittests/untitled.qml -d
    # pox -m qmlease run unittests/untitled.qml -d -v :true
    cli.run()
