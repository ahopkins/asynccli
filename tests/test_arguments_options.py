import asynccli
from decimal import Decimal
from unittest.mock import patch


class CommandWithArgTypes(asynccli.CLI):
    some_int = asynccli.Integer()
    some_float = asynccli.Float()
    some_decimal = asynccli.Decimal()
    some_str = asynccli.String()
    some_bool_1 = asynccli.Boolean()
    some_bool_2 = asynccli.Boolean()
    some_bool_3 = asynccli.Boolean()
    some_bool_4 = asynccli.Boolean()
    some_bool_5 = asynccli.Boolean()
    some_bool_6 = asynccli.Boolean()
    some_bool_7 = asynccli.Boolean()
    some_bool_8 = asynccli.Boolean()

    async def call(self, args):
        print(repr(args.some_int), 'is a int:', isinstance(args.some_int, int))
        print(repr(args.some_float), 'is a float:', isinstance(args.some_float, float))
        print(repr(args.some_decimal), 'is a Decimal:', isinstance(args.some_decimal, Decimal))
        print(repr(args.some_str), 'is a str:', isinstance(args.some_str, str))
        print(repr(args.some_bool_1), 'is a Boolean:', isinstance(args.some_bool_1, bool))
        print(repr(args.some_bool_2), 'is a Boolean:', isinstance(args.some_bool_2, bool))
        print(repr(args.some_bool_3), 'is a Boolean:', isinstance(args.some_bool_3, bool))
        print(repr(args.some_bool_4), 'is a Boolean:', isinstance(args.some_bool_4, bool))
        print(repr(args.some_bool_5), 'is a Boolean:', isinstance(args.some_bool_5, bool))
        print(repr(args.some_bool_6), 'is a Boolean:', isinstance(args.some_bool_6, bool))
        print(repr(args.some_bool_7), 'is a Boolean:', isinstance(args.some_bool_7, bool))
        print(repr(args.some_bool_8), 'is a Boolean:', isinstance(args.some_bool_8, bool))


def test_arguments_types(capsys):
    with patch('sys.argv', ['', '1', '1', '1', '1', 'True', 't', 'yes', 'y', 'YES', 'true', '1', 'False', ]):
        app = asynccli.App(CommandWithArgTypes)
        app.run()
        task = app.task_instances[0]

    out, _ = capsys.readouterr()
    assert out == "1 is a int: True\n1.0 is a float: True\nDecimal('1') is a Decimal: True\n'1' is a str: True\nTrue is a Boolean: True\nTrue is a Boolean: True\nTrue is a Boolean: True\nTrue is a Boolean: True\nTrue is a Boolean: True\nTrue is a Boolean: True\nTrue is a Boolean: True\nFalse is a Boolean: True\n"
    assert isinstance(task.arguments.some_int, int)
    assert isinstance(task.arguments.some_float, float)
    assert isinstance(task.arguments.some_decimal, Decimal)
    assert isinstance(task.arguments.some_str, str)
    assert task.arguments.some_bool_1 is True
    assert task.arguments.some_bool_2 is True
    assert task.arguments.some_bool_3 is True
    assert task.arguments.some_bool_4 is True
    assert task.arguments.some_bool_5 is True
    assert task.arguments.some_bool_6 is True
    assert task.arguments.some_bool_7 is True
    assert task.arguments.some_bool_8 is False
