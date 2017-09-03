import asyncio
import inspect
# from .cli import BaseCLI
from .arguments import Arguments


class App(object):
    def __init__(self, *tasks):
        self.loop = asyncio.get_event_loop()
        self.tasks = tasks
        self.task_instances = {}

    def run(self):
        self._initialize_tasks()
        self._setup_tasks()
        self._call_tasks()
        self._teardown_tasks()

    def _setup_tasks(self):
        self.__tasks_operation('setup')

    def _call_tasks(self):
        self.__tasks_operation('call')

    def _teardown_tasks(self):
        self.__tasks_operation('teardown')

    def _initialize_tasks(self):
        for idx, task in enumerate(self.tasks):
            if inspect.isclass(task):
                instance = task(app=self)
                self.task_instances.update({idx: instance})

    def __tasks_operation(self, operation='call'):
        tasks = []
        for idx, task in enumerate(self.tasks):
            if inspect.isclass(task):
                instance = self.task_instances.get(idx)

                method = getattr(instance, operation, None)
                if method is not None:
                    args = getattr(instance, 'arguments', Arguments())
                    tasks.append(method(args))
            else:
                if operation == 'call':
                    tasks.append(task())
        if tasks:
            self.loop.run_until_complete(asyncio.wait(tasks))
