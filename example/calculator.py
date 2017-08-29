import asynccli


class DivisionCalculator(asynccli.CLI):
    first_num = asynccli.Integer(help_text='This is some help text.')
    second_num = asynccli.Integer()

    async def call(self):
        print(self.first_num / self.second_num)


class MultiplicationCalculator(asynccli.CLI):
    first_num = asynccli.Integer(help_text='This is some help text.')
    second_num = asynccli.Integer()

    async def call(self):
        print(self.first_num * self.second_num)


class Calculator(asynccli.TieredCLI):
    d = DivisionCalculator
    m = MultiplicationCalculator


if __name__ == '__main__':
    app = asynccli.App(Calculator)
    app.run()
