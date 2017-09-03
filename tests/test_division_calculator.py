import asynccli
from unittest.mock import patch


class Calculator(asynccli.CLI):
    first_num = asynccli.Integer()
    second_num = asynccli.Integer()

    async def call(self, args):
        print(args.first_num / args.second_num)


def test_division_calculator(capsys):
    # sys.argv = ['1', '2']

    with patch('sys.argv', ['', '1', '2']):
        app = asynccli.App(Calculator)
        app.run()

    out, _ = capsys.readouterr()
    assert out == "0.5\n"
