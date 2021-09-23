import os
import django

from django.utils.module_loading import import_string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
django.setup()


def run_event(event):
    func = import_string(event["task_path"])
    return func(*event["args"], **event["kwargs"])
