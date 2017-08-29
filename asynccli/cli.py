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


class CLI(BaseCLI, metaclass=CLIMeta):
    def __init__(self, parent=None, argname=None, *args, **kwargs):
        self.parent = parent
        self.argname = argname
        super().__init__(*args, **kwargs)

    def _setup_parser(self):
        if self.parent:
            self.parser = self.parent.subparsers.add_parser(self.argname)
        else:
            self.parser = argparse.ArgumentParser()

        for name, arg in self._meta.arguments.items():
            self.parser.add_argument(
                name,
                type=arg.argtype,
                help=arg.help_text,
            )

    def _parse_args(self):
        if self.parent is None:
            self.parser.parse_args(namespace=self)
        else:
            for argname, _ in self._meta.arguments.items():
                # print(argname)
                argument = getattr(self.parent, argname, None)
                setattr(self, argname, argument)


class Subcommands(object):
    def __init__(self):
        self.command_list = []

    def __iter__(self):
        for command in self.command_list:
            yield getattr(self, command, None)

    def add(self, name, command):
        self.command_list.append(name)
        setattr(self, name, command)


class TieredCLI(BaseCLI, metaclass=TieredCLIMeta):
    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        self._setup_parser()
        self._setup_subcommands()
        self._parse_args()

    def _setup_subcommands(self):
        # self.subcommands = type('Subcommands', (object, ), {})
        self.subcommands = Subcommands()

        for argname, arg in self._meta.subcommands.items():
            command = arg(parent=self, argname=argname)
            # setattr(self.subcommands, argname, command)
            self.subcommands.add(argname, command)

    def _setup_parser(self):
        self.parser = argparse.ArgumentParser()
        self.subparsers = self.parser.add_subparsers(help='Commands', dest='command')

    def _parse_args(self):
        self.parser.parse_args(namespace=self)
        for subcommand in self.subcommands:
            subcommand._parse_args()

    async def call(self):
        command = getattr(self.subcommands, self.command)
        await command.call()
