class Argument(object):
    __slots__ = ('argtype', 'required', 'help_text')

    def __init__(
        self,
        required=False,
        help_text=None,
    ):
        self.required = required
        self.help_text = help_text


class Integer(Argument):
    argtype = int
