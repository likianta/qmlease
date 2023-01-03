from __future__ import annotations

import atexit
import time
from collections import deque
from contextlib import contextmanager
from functools import partial
from typing import AnyStr

from lk_utils import new_thread

from .__ext__ import QObject
from .__ext__ import signal
from .__ext__ import slot
from ..model import Model

_generate_timestamp = partial(time.strftime, '%H:%M:%S')


class Logger(QObject):
    short_streamed = signal(str)
    streamed = signal(str)
    
    _count: int = 0
    _long_stream_enabled: bool = True
    _message_queue: deque
    _model: Model
    _running = False
    _short_stream_enabled: bool = True
    _show_number: bool = True
    _show_time: bool = True
    
    def __init__(self):
        super().__init__()
        self._message_queue = deque()
        self._model = Model(('msg',))
        self.streamed.connect(lambda msg: self._model.append({'msg': msg}))
        self._start_streaming_loop()
        atexit.register(self._close)
    
    @property
    def enabled(self) -> bool:
        return self._short_stream_enabled or self._long_stream_enabled
    
    @slot(result=object)
    def get_model(self) -> Model:
        return self._model
    
    def pause(self, short_en=False, long_en=False) -> None:
        self._short_stream_enabled = short_en
        self._long_stream_enabled = long_en
    
    def resume(self, short_en=True, long_en=True) -> None:
        self._short_stream_enabled = short_en
        self._long_stream_enabled = long_en
    
    @contextmanager
    def on_pausing(self, short_en=False, long_en=False):
        self.pause(short_en, long_en)
        yield
        self.resume()
    
    def _close(self) -> None:
        self._short_stream_enabled = False
        self._long_stream_enabled = False
        self._running = False
        self._message_queue.clear()
        self._model.clear()
    
    # -------------------------------------------------------------------------
    
    def log(self, *msg, color='default', markup='', _async=True) -> None:
        """
         args:
             markup: additional markup except 'p' and 's'. see also markup usage
                 in `lib:lk-logger`.
                 trick: if color is 'red', the markup will auto add 'v4' tag
                 (for error style); if color is 'green', will auto add 'v2'
                 (for info style).
         """
        if not self.enabled:
            return
        if color == 'red':
            markup = 'v4' + markup
        elif color == 'green':
            markup = 'v2' + markup
        elif color == 'yellow':
            markup = 'v3' + markup
        print(f':{markup}ps', *msg)
        self._push_stream(*msg, color=color, _async=_async)
    
    @slot(str)
    def qlog(self, msg: str) -> None:
        # this is called by qml side.
        if not self.enabled: return
        self._push_stream(msg, color='raw')
        #   color='raw': the qml message may contain html tags itself, so we
        #       leave it as-is.
    
    @slot()
    def clear(self) -> None:
        self._count = 0
        self._model.clear()
    
    def _push_stream(self, *msg: str, color: str, _async=True) -> None:
        self._count += 1
        # construct output string
        msg = '; '.join(map(str, msg))
        
        # short message
        if self._short_stream_enabled:
            short_msg = self._colorify(msg, color)
        else:
            short_msg = ''
        
        # long message
        if self._long_stream_enabled:
            if self._show_time:
                msg = '[{}] {}'.format(_generate_timestamp(), msg)
            if self._show_number:
                # msg = '{:>4d}. {}'.format(self._count, msg)
                msg = '{:>3}. {}'.format(self._count, msg)
            long_msg = self._colorify(msg, color)
        else:
            long_msg = ''
        
        if _async:
            self._message_queue.append((short_msg, long_msg))
        else:
            self.short_streamed.emit(short_msg)
            self.streamed.emit(long_msg)
    
    @new_thread(singleton=True)
    def _start_streaming_loop(self) -> None:
        self._running = True
        while self._running:
            if self._message_queue:
                short, long = self._message_queue.popleft()
                if short: self.short_streamed.emit(short)
                if long: self.streamed.emit(long)
            time.sleep(0.01)
    
    # -------------------------------------------------------------------------
    
    # TODO: below colors are both high contrast in light and dark mode.
    #   but we'd better to sync it with current theme (`../../style/color.py`).
    _color_stripe = {
        'blue'   : '#202AB5',
        'grey'   : '#97A5A5',
        'green'  : '#008000',
        'magenta': '#A109A0',
        'red'    : '#FF0000',
    }
    
    def update_colors(self, **kwargs) -> None:
        self._color_stripe.update(kwargs)
    
    def _colorify(self, msg: AnyStr, color: str) -> str:
        if color == 'raw':  # see explanation in `self.qlog`.
            return '<span>{}</span>'.format(msg)
        elif color == 'default':
            return '<span>{}</span>'.format(
                msg.replace(' ', '&nbsp;').replace('\n', '<br>')
            )
        else:
            color = self._color_stripe.get(color, color)
            return '<font color="{}">{}</font>'.format(
                color, msg.replace(' ', '&nbsp;').replace('\n', '<br>')
            )
    
    # -------------------------------------------------------------------------
    # frequently used colors
    
    def red(self, *msg) -> None:
        print(':ps', *msg)
        self.streamed.emit('; '.join(
            map(lambda x: self._colorify(x, color='red'), msg)
        ))
    
    def green(self, *msg) -> None:
        print(':p', *msg)
        self.streamed.emit('; '.join(
            map(lambda x: self._colorify(x, color='green'), msg)
        ))
    
    def blue(self, *msg) -> None:
        print(':p', *msg)
        self.streamed.emit('; '.join(
            map(lambda x: self._colorify(x, color='blue'), msg)
        ))


logger = Logger()
log = logger.log
