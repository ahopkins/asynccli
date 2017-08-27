# import asynccli
import sys


def callable():
    print('hello')
    return True


def test_init(capsys):
    assert callable(), "Something wrong"
    out, err = capsys.readouterr()
    assert out == "hello\n"
