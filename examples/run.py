import os
import sys

from argsense import cli
from lk_utils import cd_current_dir
from lk_utils import run_cmd_args

cd_current_dir()
os.environ['PYTHONPATH'] = '..'  # added `qmlease`

_run_py = lambda *args, **kwargs: run_cmd_args(
    sys.executable, *args,
    verbose=True, ignore_return=True, **kwargs
)
_run_qmlease = lambda *args, **kwargs: run_cmd_args(
    sys.executable, '-m', 'qmlease', 'run', *args,
    verbose=True, ignore_return=True, **kwargs
)


# -----------------------------------------------------------------------------

@cli.cmd()
def hello_world() -> None:
    _run_py('hello_world/main.py')


@cli.cmd()
def hot_reloading() -> None:
    _run_py('hot_reloading/main.py')


if __name__ == '__main__':
    # py examples/run.py -h
    # py examples/run.py hello-world
    cli.run()
