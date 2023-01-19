"""
usage:
    run in command line:
        py -m qmlease -h
        py -m qmlease run <qml_file>
        py -m qmlease run <qml_file> --debug
        ...
"""
from argsense import cli


# from argsense import config
# config.CONSOLE_WIDTH = 120


@cli.cmd()
def run(view: str, debug=False):
    """
    Run target QML file.
    
    args:
        view: the qml file (relative or absolute path) to load.
        
    kwargs:
        debug (-d): enable hot reload.
    """
    from .application import app
    app.run(view, debug=debug)


@cli.cmd()
def list_builtin_pyhandlers():
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
    # list_ = (
    #     'pyside',
    #     'pystyle',
    #     'pyalign',
    #     'pycolor',
    #     'pyfont',
    #     'pymotion',
    #     'pysize',
    #     'pylayout',
    #     'pyrss',
    # )
    # print(':ls', list_)
    print('''
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
    ''')


if __name__ == '__main__':
    cli.run()
