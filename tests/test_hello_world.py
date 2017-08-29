import asynccli


async def mycli():
    print("Hello, world.")


class MyCLI(asynccli.CLI):
    async def call(self):
        print("Hello, world.")


def test_hello_world_basic(capsys):
    app = asynccli.App(mycli)
    app.run()

    out, _ = capsys.readouterr()
    assert out == "Hello, world.\n"


def test_hello_world_class(capsys):
    app = asynccli.App(MyCLI)
    app.run()

    out, _ = capsys.readouterr()
    assert out == "Hello, world.\n"
