import typing as t

from argsense import cli
from lk_utils import xpath

from qmlease import Model
from qmlease import QObject
from qmlease import app
from qmlease import slot
from sidework.simple_designer.loader import StylesheetLoader


class Main(QObject):
    # listview: QObject
    
    def __init__(self, stylesheet_path: str):
        super().__init__()
        self._loader = StylesheetLoader(stylesheet_path)
        self.model = Model({
            'label': '', 'color': '000000'
        })
    
    @slot()
    def reset(self) -> None:
        self.model.clear()
        print(':i0')
        for name, color in self._loader.reload().items():
            print(name, color, ':i')
            self.model.append({'label': name, 'color': color})

    @slot(str, result=object)
    def qget(self, name: str) -> t.Any:
        return getattr(self, name)

    @slot(str, object)
    def qset(self, name: str, value: t.Any) -> None:
        setattr(self, name, value)


@cli.cmd()
def main(stylesheet_path: str, debug=True) -> None:
    main_prog = Main(stylesheet_path)
    app.register(main_prog, 'main')
    app.run(xpath('qml/Main.qml'), debug=debug)


if __name__ == '__main__':
    cli.run(main)
