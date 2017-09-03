import argparse
import asyncio
import signal

from .arguments import Argument, Arguments
from .commands import Subcommands
from collections import OrderedDict


class BaseMeta(type):
    @classmethod
    def __prepare__(mcs, cls, bases):
        return OrderedDict()


class CLIMeta(BaseMeta):
    def __new__(mcs, name, bases, attrs):
        obj = super().__new__(mcs, name, bases, attrs)
        obj._meta = type('CLIMeta', (object, ), {
            'command': True,
            'arguments': obj._get_arguments(attrs),
            'bases': bases,
        })
        return obj

    @staticmethod
    def _get_arguments(attrs):
        args = [
            (argname, arg) for argname, arg in attrs.items()
            if isinstance(arg, Argument)
        ]
        return OrderedDict(args)


class TieredCLIMeta(BaseMeta):
    def __new__(mcs, name, bases, attrs):
        obj = super().__new__(mcs, name, bases, attrs)
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
                # if 'CLI' in qualnames:
                if 'CLI' in qualnames or 'TieredCLI' in qualnames:
                    subcommands.append((argname, arg))

        # print(subcommands)
        return OrderedDict(subcommands)


class BaseCLI(object):
    __slots__ = ('_meta', 'call', 'app')

    def __init__(self, app=None, *args, **kwargs):
        self.app = app
    #     signal.signal(signal.SIGINT, self.exit_gracefully)
    #     signal.signal(signal.SIGTERM, self.exit_gracefully)
    #     self.running = True
    #     self.loop = loop

    # def graceful(self):
    #     return self.running

    # def exit_gracefully(self, *args, **kwargs):
    #     """Execute the Graceful exit sequence

    #     See:
    #     https://stackoverflow.com/questions/37417595/graceful-shutdown-of-asyncio-coroutines#37430948
    #     https://stackoverflow.com/questions/33357233/when-to-use-and-when-not-to-use-python-3-5-await/33399896#33399896
    #     https://github.com/wikibusiness/async_armor

    #     Arguments:
    #         *args {[type]} -- [description]
    #         **kwargs {[type]} -- [description]
    #     """
    #     print('Gracefully shutting down')
    #     self.loop.stop()
    #     pending = asyncio.Task.all_tasks()
    #     print(pending)
    #     self.loop.run_until_complete(asyncio.gather(*pending))
    #     print('Graceful shutdown complete')
    #     self.running = False


class CLI(BaseCLI, metaclass=CLIMeta):
    def __init__(self, parent=None, argname=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.argname = argname
        self._setup_parser()
        self._parse_args()

        if self.parent:
            self.app = self.parent.app

    def _setup_parser(self):
        if self.parent:
            # print('parent: ', self.parent.subparsers)
            self.parser = self.parent.subparsers.add_parser(self.argname)
        else:
            self.parser = argparse.ArgumentParser()

        for name, arg in self._meta.arguments.items():
            # TODO:
            # - flesh our options stored on arg
            self.parser.add_argument(
                arg.get_name(name),
                type=arg.get_type(),
                help=arg.help,
            )

    def _parse_args(self):
        if self.parent is None:
            self.arguments = Arguments()
            self.parser.parse_args(namespace=self.arguments)
        # else:
        #     self.arguments = self.parent.arguments
        # else:
        #     self.arguments = Arguments()
        #     # print(dir(self.parent.arguments))
        #     # print(self.parent.arguments)
        #     for argname in self.parent.arguments.argument_list:
        #         argument = getattr(self.parent.arguments, argname, None)
        #         print(argname, argument)
        #         setattr(self.arguments, argname, argument)
        # #     # for argname, _ in self._meta.arguments.items():
        # #     #     argument = getattr(self.parent.arguments, argname, None)
        # #     #     setattr(self, argname, argument)


class TieredCLI(BaseCLI, metaclass=TieredCLIMeta):
    def __init__(self, parent=None, argname=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.argname = argname
        self._setup_parser()
        self._setup_subcommands()
        self._parse_args()

    def _get_dest(self):
        if self.argname:
            return '{}_commands'.format(self.argname)
        else:
            return 'commands'

    def _get_help(self):
        if self.argname:
            return '{} Commands'.format(self.argname.title())
        else:
            return 'Commands'

    def _get_parser_name(self):
        if self.argname:
            return self.argname
        else:
            return 'parser'

    def _setup_subcommands(self):
        self.subcommands = Subcommands()
        self.arguments = Arguments()

        for argname, command in self._meta.subcommands.items():
            command = command(parent=self, argname=argname)

            if self.parent:
                self.parent.subcommands.add(argname, command)
            else:
                self.subcommands.add(argname, command)

    def _setup_parser(self):
        if self.parent is None:
            self.parser = argparse.ArgumentParser()
        else:
            self.parser = self.parent.subparsers.add_parser(self._get_parser_name())
        self.subparsers = self.parser.add_subparsers(
            help=self._get_help(),
            # dest=self._get_dest(),
            dest='command',
        )

    def _parse_args(self):
        if self.parent is None:
            self.parser.parse_args(namespace=self.arguments)
            for subcommand in self.subcommands:
                subcommand._parse_args()
        else:
            # print(dir(self.parprintent.arguments))
            # print(self.parent.printarguments)
            for argname in self.parent.arguments.argument_list:
                argument = getattr(self.parent.arguments, argname, None)
                # print(argnameprint, argument)
                setattr(self, argname, argument)

    async def call(self, _):
        if getattr(self.arguments, 'command', None) is not None:
            command = getattr(self.subcommands, self.arguments.command)
            await command.call(self.arguments)
