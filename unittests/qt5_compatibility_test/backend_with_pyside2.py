"""
test if is there any error when import qmlease backended with pyside2.
"""
import os
os.environ['QT_API'] = 'pyside2'

from lk_utils import xpath
from qmlease import app
app.run(xpath('backend_with_pyside2.qml'))
