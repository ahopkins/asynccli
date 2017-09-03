import asynccli
from unittest.mock import patch


class DivisionCalculator(asynccli.CLI):
    first_num = asynccli.Integer()
    second_num = asynccli.Integer()

    async def call(self, args):
        print(args.first_num / args.second_num)


class MultiplicationCalculator(asynccli.CLI):
    first_num = asynccli.Integer()
    second_num = asynccli.Integer()

    async def call(self, args):
        print(args.first_num * args.second_num)


class Calculator(asynccli.TieredCLI):
    d = DivisionCalculator
    m = MultiplicationCalculator


def test_calculator_with_multiplication(capsys):
    with patch('sys.argv', ['', 'm', '2', '4']):
        app = asynccli.App(Calculator)
        app.run()

    out, _ = capsys.readouterr()
    assert out == "8\n"


def test_calculator_with_division(capsys):
    with patch('sys.argv', ['', 'd', '2', '4']):
        app = asynccli.App(Calculator)
        app.run()

    out, _ = capsys.readouterr()
    assert out == "0.5\n"
