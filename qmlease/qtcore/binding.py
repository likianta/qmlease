import typing as t

from .qobject import QObject


def bind(src: QObject, tar: QObject,
         src_attr: str, tar_attr: str = None,
         extra_func=None) -> None:
    from ..qmlside import eval_js
    
    if tar_attr is None: tar_attr = src_attr
    
    if extra_func is None:
        eval_js('''
            $tar.{tar_attr} = Qt.binding(() => $src.{src_attr})
        ''', {'tar': tar, 'tar_attr': tar_attr,
              'src': src, 'src_attr': src_attr})
    else:
        raise NotImplementedError


def bind_func(qobj: QObject, signal: str, func: t.Callable) -> None:
    eval('qobj.{signal}.connect(func)'.format(signal=signal),
         {'qobj': qobj, 'func': func})
