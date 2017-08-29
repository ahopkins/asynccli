import asynccli


async def mycli():
    print("Hello, world.")


class MultiplicationCalculator(asynccli.CLI):
    first_num = asynccli.Integer(help_text='This is some help text.')
    second_num = asynccli.Integer()

    async def call(self):
        print(self.first_num * self.second_num)


class Calculator(asynccli.TieredCLI):
    m = MultiplicationCalculator


if __name__ == '__main__':
    app = asynccli.App(Calculator, mycli)
    app.run()
