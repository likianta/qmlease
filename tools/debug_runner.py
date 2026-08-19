import os
import sys
import typing as tp
from time import sleep

from argsense import cli
from lk_utils import run_cmd_args
from lk_utils import run_new_thread
from lk_utils.subproc import Popen
from neoprint import bprint  # the built-in print function
from neoprint import print


@cli
def run(
    entry_script: str, timeout_starts: int = 5, timeout_ends: int = 15
) -> None:
    """
    Run target application and inspects the terminal output.

    This tool is used for AI to control the whole process of GUI without
    clicking app window or pressing Ctrl+C to finish the test. Instead, it
    observes the key message to know if the test starts or finishes.

    The `entry_script` is a ".py" file, which contains `test_ui` method, you can
    get an example at `test/debug_running_app.py`.

    In `test_ui`, it must contain two print statements:
        import qmlease as qe
        class TestFramework(qe.QObject):
            @qe.Slot(object)
            def test_ui(self, window: qe.QObject) -> None:
                print('TEST UI START')  # must be uppercase
                ...
                print('TEST UI END')  # must be uppercase
                QTimer.singleShot(0, qe.app.quit)
        ...
    """
    os.environ['QMLEASE_ZERO_TOLERANCE_EXCEPTION'] = '1'
    proc = tp.cast(
        Popen,
        run_cmd_args(
            (sys.executable, entry_script), verbose=True, blocking=False
        ),
    )
    proc.communication_thread = run_new_thread(
        _communication, proc.stdout, daemon=False, interruptible=True
    )
    _watch_key_status(proc, timeout_starts, timeout_ends)


_flag = 0  # 0: not started; 1: starts testing ui; 2: end testing ui


def _watch_key_status(
    process: Popen, timeout_starts: int = 5, timeout_ends: int = 15
) -> None:
    time_elapsed = 0.0
    while True:
        if process.is_alive:
            if process.stderr:
                print(':v8', 'process exit with error')
                break
            if _flag == 0:
                if time_elapsed > timeout_starts:
                    process.kill()
                    raise Exception('timeout waitng for "TEST UI START"')
            elif _flag == 1:
                if time_elapsed > timeout_ends:
                    process.kill()
                    raise Exception('timeout waitng for "TEST UI END"')
        else:
            print('process exit', ':v')
            break
        sleep(0.1)
        time_elapsed += 0.1


def _communication(stdout: tp.IO) -> tp.Generator:

    def readlines(source: tp.IO) -> tp.Iterator[str]:
        last: bytes = b''
        curr: bytes
        temp: bytes = b''
        while True:
            try:
                if curr := source.read(1):
                    if curr == b'\n':
                        temp += curr
                        yield temp.decode(errors='ignore')
                        temp = b''
                    elif last == b'\r':
                        yield temp.decode(errors='ignore')
                        temp = curr
                    else:
                        temp += curr
                    last = curr
                else:
                    break
            except Exception as e:
                print(':e', e)
                break
        if temp:
            yield (temp + b'\n').decode(errors='ignore')

    for line in readlines(stdout):
        bprint(line, end='', flush=True)
        _check_key_message(line)
        yield


def _check_key_message(line: str) -> int:
    global _flag
    if _flag == 0:
        if 'TEST UI START' in line:
            _flag = 1
    elif _flag == 1:
        if 'TEST UI END' in line:
            _flag = 2
    return _flag


if __name__ == '__main__':
    # python tools/debug_runner.py -h
    # python tools/debug_runner.py test/debug_running_app.py
    # python tools/debug_runner.py examples/register_access_editor/app.py
    cli.run(run)
