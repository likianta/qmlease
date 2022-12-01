from __future__ import annotations

from argsense import cli


@cli.cmd()
def main(target_file: str | None, app_name: str = None):
    """
    args:
        target_file: path to the qml file.
            if you don't provide the file, i.e. you want just to have a look -
            at the reloader gui, you can pass [magenta]":none"[/] to the param.
    kwargs:
        app_name: optional. if not set, will use hot reloader's default name -
            ([magenta]"LK Hot Reloader"[/]).
    """
    from .hot_reloader import HotReloader
    reloader = HotReloader(app_name or 'LK Hot Reloader')
    if target_file is None:
        reloader.dry_run()
    else:
        reloader.run(target_file)


if __name__ == '__main__':
    cli.run(main)
