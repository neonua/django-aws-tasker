import boto3
import botocore.exceptions
import json

from .constants import LAMBDA_ASYNC_PAYLOAD_LIMIT
from .exceptions import *


ASYNC_RESPONSE_TABLE = None

# Declare these here so they're kept warm.
try:
    aws_session = boto3.Session()
    LAMBDA_CLIENT = aws_session.client('lambda')
except botocore.exceptions.NoRegionError as e:  # pragma: no cover
    # This can happen while testing on Travis, but it's taken care  of
    # during class initialization.
    pass


class Task:
    name = None
    typing = None
    backend = None  # TODO: add result backend

    capture_response = None
    lambda_function_name = None,
    aws_region = None,

    throws = ()

    abstract = True

    _exec_options = None

    _backend = None  # set by backend property.

    @classmethod
    def add_around(cls, attr, around):
        orig = getattr(cls, attr)
        if getattr(orig, '__wrapped__', None):
            orig = orig.__wrapped__
        meth = around(orig)
        meth.__wrapped__ = orig
        setattr(cls, attr, meth)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        raise NotImplementedError('Tasks must define the run method.')

    def delay(self, *args, **kwargs):
        return self.apply_async(args, kwargs)

    def apply_async(self, args=None, kwargs=None):
        # TODO: add task_always_eager
        task_path = f'{self.__module__}.{self.__name__}'
        send_result = LambdaAsyncResponse(
            lambda_function_name=self.lambda_function_name,
            aws_region=self.aws_region,
            capture_response=self.capture_response,
        ).send(task_path, args, kwargs)
        return send_result

    @property
    def __name__(self):
        return self.__class__.__name__


class LambdaAsyncResponse:
    def __init__(
        self,
        lambda_function_name=None,
        aws_region=None,
        # TODO: add capture_response
        **kwargs
    ):
        """ """
        if kwargs.get('boto_session'):
            self.client = kwargs.get('boto_session').client('lambda')
        else:
            self.client = LAMBDA_CLIENT

        self.lambda_function_name = lambda_function_name
        self.aws_region = aws_region

    def send(self, task_path, args, kwargs):
        """
        Create the message object and pass it to the actual sender.
        """
        message = {
            'task_path': task_path,
            'args': args,
            'kwargs': kwargs,
        }
        self._send(message)
        return self

    def _send(self, message):
        """
        Given a message, directly invoke the lamdba function for this task.
        """
        message['command'] = 'django_aws_tasker.routes.route_lambda_task'
        payload = json.dumps(message).encode("utf-8")

        if len(payload) > LAMBDA_ASYNC_PAYLOAD_LIMIT:  # pragma: no cover
            raise AsyncException('Payload too large for async Lambda call')

        self.response = self.client.invoke(
            FunctionName=self.lambda_function_name,
            InvocationType='Event',
            Payload=payload,
        )
        self.sent = self.response.get("StatusCode", 0) == 202



