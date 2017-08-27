import asynccli


class MyCLI(asynccli.CLI):
    async def call(self):
        print("Hello, world.")


if __name__ == '__main__':
    app = asynccli.App(MyCLI)
    app.run()
