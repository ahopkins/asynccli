from .arguments import Argument
import argparse
import sys
from collections import OrderedDict
# from pprint import pprint


class BaseMeta(type):
    @classmethod
    def __prepare__(mcls, cls, bases):
        return OrderedDict()


class CLIMeta(BaseMeta):
    def __new__(cls, name, bases, attrs):
        obj = super().__new__(cls, name, bases, attrs)
        obj._meta = type('CLIMeta', (object, ), {
            'command': True,
            'arguments': obj._get_arguments(attrs),
            'bases': bases,
        })
        return obj

    @staticmethod
    def _get_arguments(attrs):
        return OrderedDict([(argname, arg) for argname, arg in attrs.items() if isinstance(arg, Argument)])


class TieredCLIMeta(BaseMeta):
    def __new__(cls, name, bases, attrs):
        obj = super().__new__(cls, name, bases, attrs)
        obj._meta = type('TieredCLIMeta', (object, ), {
            'command': False,
            'subcommands': obj._get_subcommands(attrs, bases),
            'bases': bases,
        })
        return obj

    @staticmethod
    def _get_subcommands(attrs, bases):
        subcommands = []
        qualnames = [base.__qualname__ for base in bases]

        if 'TieredCLI' not in qualnames:
            return None

        for argname, arg in attrs.items():
            if hasattr(arg, '_meta'):
                qualnames = [base.__qualname__ for base in arg._meta.bases]
                if 'CLI' in qualnames:
                    subcommands.append((argname, arg))

        return OrderedDict(subcommands)


class BaseCLI(object):
    __slots__ = ('_meta', 'call')

    def __init__(self):
        self._setup_parser()
        self._parse_args()

    def _setup_parser(self):
        self.parser = None
        assert self.parser, "_setup_parser not defined"

    def _parse_args(self):
        self.parser.parse_args(namespace=self)


class CLI(BaseCLI, metaclass=CLIMeta):
    def _setup_parser(self):
        self.parser = argparse.ArgumentParser()

        for name, arg in self._meta.arguments.items():
            self.parser.add_argument(
                name,
                type=arg.argtype,
                help=arg.help_text,
            )


class TieredCLI(BaseCLI, metaclass=TieredCLIMeta):
    def _setup_parser(self):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument(
            'command',
            type=str,
        )

        self.parser.add_argument(
            'arguments',
            nargs='+',
        )

    async def call(self):
        cmd = self._meta.subcommands.get(self.command, None)

        if cmd is None:
            raise Exception('Could not find command {}'.format(self.command))

        del sys.argv[1]

        command = cmd()
        await command.call()
