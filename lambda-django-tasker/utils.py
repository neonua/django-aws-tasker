import importlib
import sys
import inspect


def import_and_get_task(task_path):
    """
    Given a modular path to a function, import that module
    and return the function.
    """
    module, function = task_path.rsplit(".", 1)
    app_module = importlib.import_module(module)
    app_function = getattr(app_module, function)
    return app_function


def get_func_task_path(func):
    """
    Format the modular task path for a function via inspection.
    """
    module_path = inspect.getmodule(func).__name__
    task_path = f'{module_path}.{func.__name__}'
    return task_path


def gen_task_name(name, module_name):
    module_name = module_name or '__main__'
    module = sys.modules.get(module_name)

    if module:
        module_name = module.__name__
    if module_name == '__main__':
        return '.'.join(['__main__', name])
    return '.'.join(p for p in (module_name, name) if p)
