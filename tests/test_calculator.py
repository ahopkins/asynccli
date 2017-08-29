import asynccli
from unittest.mock import patch


class DivisionCalculator(asynccli.CLI):
    first_num = asynccli.Integer(help_text='This is some help text.')
    second_num = asynccli.Integer()

    async def call(self):
        print(self.first_num / self.second_num)


class MultiplicationCalculator(asynccli.CLI):
    first_num = asynccli.Integer(help_text='This is some help text.')
    second_num = asynccli.Integer()

    async def call(self):
        print(self.first_num * self.second_num)


class Calculator(asynccli.TieredCLI):
    d = DivisionCalculator
    m = MultiplicationCalculator


def test_calculator_with_multiplication(capsys):
    with patch('sys.argv', ['', 'm', '2', '4']):
        app = asynccli.App(Calculator)
        app.run()

    out, err = capsys.readouterr()
    assert out == "8\n"


def test_calculator_with_division(capsys):
    with patch('sys.argv', ['', 'd', '2', '4']):
        app = asynccli.App(Calculator)
        app.run()

    out, err = capsys.readouterr()
    assert out == "0.5\n"
