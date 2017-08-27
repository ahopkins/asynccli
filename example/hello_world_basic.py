import asynccli


async def mycli():
    print("Hello, world.")


if __name__ == '__main__':
    app = asynccli.App(mycli)
    app.run()
