import asynccli
import asyncio


class MyCLI(asynccli.CLI):
    async def setup(self):
        print('setup')
        await asyncio.sleep(3)

    async def teardown(self):
        print('teardown')
        await asyncio.sleep(3)

    async def call(self):
        print("Hello, world.")


if __name__ == '__main__':
    app = asynccli.App(MyCLI)
    app.run()
