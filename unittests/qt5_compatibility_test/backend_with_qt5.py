"""
test if is there any error when import qmlease backended with pyside2/pyqt5.
"""
import os

from argsense import cli
from lk_utils import xpath


@cli.cmd()
def main(api: str):
    """
    args:
        api: 'pyside2' or 'pyqt5'
    """
    os.environ['QT_API'] = api
    from qmlease import QT_API, app
    print(QT_API)
    app.run(xpath('backend_with_qt5.qml'))


if __name__ == '__main__':
    cli.run(main)
