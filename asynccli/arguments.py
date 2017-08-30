class Argument(object):
    __slots__ = (
        'argtype',
        'required',
        'help',
    )

    def __init__(
        self,
        required=False,
        help=None,
    ):
        self.required = required
        self.help = help


class Integer(Argument):
    argtype = int


class String(Argument):
    argtype = str

# parser.register('type', 'bool', (lambda x: x.lower() in ("yes", "true", "t", "1")))
# parser.add_argument('--feature', type=lambda s: s.lower() in ['true', 't', 'yes', '1'])
# feature.add_argument('--feature',action='store_true')
