from .arguments import Argument
import argparse


class CLIMeta(type):
    def __new__(cls, name, bases, attrs):
        obj = super().__new__(cls, name, bases, attrs)
        obj._meta = type('CLIMeta', (object, ), {
            'arguments': obj.__get_arguments(attrs)
        })
        return obj

    def __get_arguments(self, attrs):
        return {argname: arg for argname, arg in attrs.items() if isinstance(arg, Argument)}


class CLI(object, metaclass=CLIMeta):
    __slots__ = ('_meta', 'call')

    def __init__(self):
        self.__setup_parser()
        self.__parse_args()
        # print(self._meta.arguments)

    def __setup_parser(self):
        # print(self._meta.arguments)
        self.parser = argparse.ArgumentParser()

        for name, arg in self._meta.arguments.items():
            self.parser.add_argument(
                name,
                # required=arg.required,
                type=arg.argtype,
                help=arg.help_text,
            )

    def __parse_args(self):
        self.parser.parse_args(namespace=self)
        # for arg in args.items():
        #     print(arg)
