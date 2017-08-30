import asynccli
import asyncio


class MyCLI(asynccli.CLI):
    async def setup(self):
        print('setup')
        await asyncio.sleep(1)

    async def teardown(self):
        print('teardown')
        await asyncio.sleep(1)

    async def call(self):
        print("Hello, world.")


def test_setup_teardown(capsys):
    app = asynccli.App(MyCLI)
    app.run()

    out, _ = capsys.readouterr()
    assert out == "setup\nHello, world.\nteardown\n"
