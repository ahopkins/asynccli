import asynccli
import asyncio


class MyCLI(asynccli.CLI):
    async def setup(self, args):
        print('setup')
        await asyncio.sleep(3)

    async def teardown(self, args):
        print('teardown')
        await asyncio.sleep(3)

    async def call(self, args):
        print("Hello, world.")


if __name__ == '__main__':
    app = asynccli.App(MyCLI)
    app.run()
