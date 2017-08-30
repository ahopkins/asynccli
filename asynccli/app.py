import asyncio
import inspect
from .cli import BaseCLI


class App(object):
    def __init__(self, *tasks):
        self.loop = asyncio.get_event_loop()
        self.tasks = tasks

    def run(self):
        self._setup_tasks()
        self._call_tasks()
        self._teardown_tasks()

    def _setup_tasks(self):
        self.__tasks_operation('setup')

    def _call_tasks(self):
        self.__tasks_operation('call')

    def _teardown_tasks(self):
        self.__tasks_operation('teardown')

    def __tasks_operation(self, operation='call'):
        tasks = []
        for task in self.tasks:
            if inspect.isclass(task) or operation == 'call':
                called = task()
                if isinstance(called, BaseCLI):
                    method = getattr(called, operation, None)
                    if method is not None:
                        tasks.append(method())
                else:
                    tasks.append(called)
        if tasks:
            self.loop.run_until_complete(asyncio.wait(tasks))
