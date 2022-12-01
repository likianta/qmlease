from argsense import cli

from .mini_producer import main as produce

cli.add_cmd(produce, 'produce')

if __name__ == '__main__':
    cli.run(produce)
