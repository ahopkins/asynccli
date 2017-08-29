import asynccli
from unittest.mock import patch


class Calculator(asynccli.CLI):
    first_num = asynccli.Integer(help_text='This is some help text.')
    second_num = asynccli.Integer()

    async def call(self):
        print(self.first_num / self.second_num)


def test_division_calculator(capsys):
    # sys.argv = ['1', '2']

    with patch('sys.argv', ['', '1', '2']):
        app = asynccli.App(Calculator)
        app.run()

    out, err = capsys.readouterr()
    assert out == "0.5\n"
