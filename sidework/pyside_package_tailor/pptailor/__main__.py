from argsense import cli

from .main import restore
from .main import tailor

cli.add_cmd(tailor)
cli.add_cmd(restore)

if __name__ == '__main__':
    cli.run()
