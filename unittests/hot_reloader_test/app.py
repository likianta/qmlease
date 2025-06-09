from argsense import cli
from lk_utils import xpath
from qmlease import app


@cli
def main(windowed: bool = False) -> None:
    # app.run(xpath('windowed.qml'))
    # app.run(xpath('windowless.qml'), debug=True)
    app.run(xpath('windowed.qml' if windowed else 'windowless.qml'), debug=True)


if __name__ == '__main__':
    cli.run(main)
