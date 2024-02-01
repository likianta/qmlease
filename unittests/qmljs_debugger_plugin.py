# py unittests/qmljs_debugger_plugin.py
import os
os.environ['QMLEASE_DEBUG_JS'] = '1'

from lk_utils import cd_current_dir
from qmlease import app

cd_current_dir()
app.run('../examples/hello_world/view.qml')
