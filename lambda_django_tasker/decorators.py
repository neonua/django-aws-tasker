from task import Task
from utils import gen_task_name


def task(*args, **kwargs):
    lambda_function_name_arg = kwargs.get('lambda_function_name_arg', 'worldskate-backend-dev-tasks')
    aws_region_arg = kwargs.get('remote_aws_region')
    # TODO: add capture_response

    def inner_create_task_cls(**opts):

        def _create_task_cls(fun):
            name = gen_task_name(fun.__name__, fun.__module__)

            run = staticmethod(fun)
            task = type(fun.__name__, (Task,), dict({
                'name': name,
                'run': run,
                'lambda_function_name': lambda_function_name_arg,
                'aws_region': aws_region_arg,
                '_decorated': True,
                '__doc__': fun.__doc__,
                '__module__': fun.__module__,
                '__annotations__': fun.__annotations__,
                '__wrapped__': run
            }, **opts))()

            try:
                task.__qualname__ = fun.__qualname__
            except AttributeError:
                pass

            return task

        return _create_task_cls

    if len(args) == 1:
        if callable(args[0]):
            return inner_create_task_cls(**kwargs)(*args)
        raise TypeError('argument 1 to @task() must be a callable')
    if args:
        raise TypeError(
            '@task() takes exactly 1 argument ({} given)'.format(
                sum([len(args), len(kwargs)])))
    return inner_create_task_cls(**kwargs)
