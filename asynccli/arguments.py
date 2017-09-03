from decimal import Decimal

DEFAULTS = {
    'option': False
}


class Arguments(object):
    def __init__(self):
        self.argument_list = set()

    def __repr__(self):
        return '<Arguments {}>'.format(self.argument_list)

    def __iter__(self):
        for argument in self.argument_list:
            yield getattr(self, argument, None)

    def __setattr__(self, key, value):
        if key != 'argument_list':
            self.argument_list.add(key)
        super().__setattr__(key, value)


class Argument(object):
    __slots__ = (
        'action',
        'argtype',
        'const',
        'default',
        'help',
        'nargs',
        'required',
        'option',
    )

    def __init__(self, *args, **kwargs):
        for key, value in DEFAULTS.items():
            setattr(self, key, value)
        for kwarg, value in kwargs.items():
            if kwarg in self.__slots__:
                setattr(self, kwarg, value, self.__get_default_value(kwarg))
        # TEMP
        self.help = None

    @staticmethod
    def __get_default_value(kwarg, default=None):
        print('kwarg', DEFAULTS.get(kwarg, default))
        return DEFAULTS.get(kwarg, default)

    def get_type(self):
        return self.argtype

    def get_name(self, name):
        prefix = '-' if self.option else ''
        return '{}{}'.format(prefix, name)


class Integer(Argument):
    __slots__ = ()
    argtype = int


class Float(Argument):
    __slots__ = ()
    argtype = float


class Decimal(Argument):
    __slots__ = ()
    argtype = Decimal


class String(Argument):
    __slots__ = ()
    argtype = str


class Boolean(Argument):
    def get_type(self):
        return lambda x: x.lower() in ['true', 't', 'yes', '1', 'y']

# parser.register('type', 'bool', (lambda x: x.lower() in ("yes", "true", "t", "1")))
# parser.add_argument('--feature', type=lambda s: s.lower() in ['true', 't', 'yes', '1'])
# feature.add_argument('--feature',action='store_true')
