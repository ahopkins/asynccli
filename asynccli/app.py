import asyncio
from .cli import CLI


class App(object):
    def __init__(self, *tasks):
        self.loop = asyncio.get_event_loop()
        self.tasks = tasks

    def run(self):
        tasks = self.__call_tasks()
        self.loop.run_until_complete(asyncio.wait(tasks))
        # self.loop.close()

    def __call_tasks(self):
        tasks = []
        for task in self.tasks:
            called = task()
            if isinstance(called, CLI):
                tasks.append(called.call())
            else:
                tasks.append(called)

        return tasks
