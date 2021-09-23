from receiver import run_event


def route_lambda_task(event, context):
    """
    Deserialises the message from event passed to zappa.handler.run_function
    imports the function, calls the function with args
    """
    print('WOW2')
    return run_event(event)

# TODO: add SQS route
