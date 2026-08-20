"""
Translate qmlease/widgets/QmlEase/Layouts/Row.qml to Column.qml
"""

import difflib

from argsense import cli
from lk_utils import dump
from lk_utils import here
from lk_utils import load
from lk_utils import manipulate_text
from neoprint import print


@cli
def main(show_diff: bool = True) -> None:
    text_i = load('qmlease/widgets/QmlEase/Layouts/Row.qml', 'plain')
    # fmt: off
    text_o = (
        manipulate_text(text_i)
        .prepend(
            '// This file was auto translated from ./Row.qml, please do not \n'
            '// modify it manuall.\n'
            '// Translator: sidework/translate_row_to_column.py\n\n'
        )
        .replacex_all(r'\brow\.', r'column.')
        # update halign comment
        .find("halign: 'start'")
        .then_findx(r'// .+').replace('// start, stretch, center')
        # update valign comment
        .then_find("valign: 'start'")
        .then_findx(r'// .+').replace('// start, stretch')
        # translate `computeLayout` function
        .reset_index()
        .find('function computeLayout').then_find('return').end().cut()
        .find('V.Rectangle').cut()
        .swap('// horizontal', '// vertical')
        .swapx(r'root\.halign\b', r'root\.valign\b')
        .swap('Width', 'Height')
        .swap('.width', '.height')
        .swap('leftPadding', 'topPadding')
        .swap('rightPadding', 'bottomPadding')
        .replace('verticalCenter', 'horizontalCenter')
        .replace('child.y', 'child.x')
        # translate real container
        .find('V.Rectangle')
        .find('Row').replace('Column')
        .then_find('id: row').replace('id: column')
        # translate `onCompleted` stage
        .then_find('Component.onCompleted')
        .replace_all('row', 'column')
        .output()
    )
    # fmt: on

    dump(text_o, 'qmlease/widgets/QmlEase/Layouts/Column.qml')

    if show_diff:
        # diff = difflib.unified_diff(
        #     text_i.splitlines(),
        #     text_o.splitlines(),
        #     fromfile='input_row.qml',
        #     tofile='output_col.qml',
        # )
        # dump(diff, here('io_diff.txt'))

        diff = difflib.HtmlDiff().make_file(
            text_i.splitlines(), text_o.splitlines()
        )
        dump(diff, here('_row_to_column_diff.html'))
        print('see "Column.qml" and "_row_to_column_diff.html"', ':v4')
    else:
        print('see "Column.qml"', ':v4')


if __name__ == '__main__':
    cli.run(main)
