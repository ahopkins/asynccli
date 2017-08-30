class Subcommands(object):
    def __init__(self):
        self.command_list = []

    def __iter__(self):
        for command in self.command_list:
            yield getattr(self, command, None)

    def add(self, name, command):
        self.command_list.append(name)
        setattr(self, name, command)
