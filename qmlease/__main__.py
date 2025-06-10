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
def run(qml_file: str, debug: bool = False) -> None:
    """
    run target QML file.
    
    params:
        debug (-d): enable hot reload.
    """
    from .application import app
    app.run(qml_file, debug=debug)


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
    cli.run()
