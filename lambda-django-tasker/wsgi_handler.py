from django.utils.module_loading import import_string

IGNORE_SOURCES = (
    'serverless-plugin-warmup',
)


def handler_tasks(event, context):
    print('WOW_NO')
    if event.get('source') in IGNORE_SOURCES:
        return {'statusCode': 200, 'body': 'Warmup'}

    print('WOW3')

    if event.get('command'):
        print('WOW4')
        whole_function = event['command']
        app_function = import_string(whole_function)
        result = app_function(event, context)
        print(f'Result of {whole_function}:')
        print(result)

    return {'statusCode': 200, 'body': 'Done'}
