from argsense import cli
from lk_utils import fs
from lk_utils import run_cmd_args


@cli
def get_help():
    run_cmd_args(
        (
            fs.there('../.venv/Lib/site-packages/PySide6/qmllint.exe'),
            '-I',
            fs.there('../qmlease/widgets'),
            '--help',
        ),
        verbose=True,
    )


@cli
def check(path: str) -> None:
    """
    Args:
        path: One or more paths to qml files.
            You can give absolute paths or paths relative to current working
            directory.
            For multiple paths, use "<path1>;<path2>;<path3>;..." format.
    """

    run_cmd_args(
        (
            fs.there('../.venv/Lib/site-packages/PySide6/qmllint.exe'),
            '--qmldirs',
            fs.there('../qmlease/widgets'),
            *path.split(';'),
        ),
        verbose=True,
    )


if __name__ == '__main__':
    # python tools/qmllint.py get_help
    # python tools/qmllint.py check examples/click_counter.qml
    # python tools/qmllint.py check \
    #   "examples/click_counter.qml;examples/sidebar/sidebar.qml"
    cli.run()
