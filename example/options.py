import asynccli


class MyCLI(asynccli.CLI):
    opt1 = asynccli.Boolean(option=True)

    async def call(self):
        print(repr(self.opt1))


if __name__ == '__main__':
    app = asynccli.App(MyCLI)
    app.run()
