def callable():
    print('hello')
    return True


def test_init(capsys):
    assert callable(), "Something wrong"
    out, _ = capsys.readouterr()
    assert out == "hello\n"
