import asynccli
from decimal import Decimal


class MyCLI(asynccli.CLI):
    some_int = asynccli.Integer()
    some_float = asynccli.Float()
    some_decimal = asynccli.Decimal()
    some_str = asynccli.String()
    some_bool_1 = asynccli.Boolean()

    async def call(self, args):
        # args = self.arguments
        print(repr(args.some_int), 'is a int:', isinstance(args.some_int, int))
        print(repr(args.some_float), 'is a float:', isinstance(args.some_float, float))
        print(repr(args.some_decimal), 'is a Decimal:', isinstance(args.some_decimal, Decimal))
        print(repr(args.some_str), 'is a str:', isinstance(args.some_str, str))
        print(repr(args.some_bool_1), 'is a Boolean:', isinstance(args.some_bool_1, bool))


if __name__ == '__main__':
    app = asynccli.App(MyCLI)
    app.run()
