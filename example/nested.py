import asynccli


class Command1(asynccli.CLI):
    foo = asynccli.String()

    async def call(self, args):
        print('foo command 1: {}'.format(args.foo))


class Level2CLI(asynccli.CLI):
    foo = asynccli.String()

    async def call(self, args):
        print('foo: {}'.format(args.foo))


class Level2BCLI(asynccli.CLI):
    bar = asynccli.String()

    async def call(self, args):
        print('bar: {}'.format(args.bar))


class Level1CLI(asynccli.TieredCLI):
    level2 = Level2CLI
    level2b = Level2BCLI


class MyCLI(asynccli.TieredCLI):
    level1 = Level1CLI
    command1 = Command1


if __name__ == '__main__':
    app = asynccli.App(MyCLI)
    app.run()
