#!/usr/bin/env python
import os
import signal
import sys
import time

from django.conf import settings

from filedb.middleware import GracefulShutdownMiddleware


def signal_handler(signum, frame):
    GracefulShutdownMiddleware.shutdown_flag = True
    count = 0
    # Таймаут на 60 секунд
    while GracefulShutdownMiddleware.post_flag and count < 60:
        time.sleep(1)
        count += 1
    if settings.configured:
        from filedb.models import File
        File.cleanup_on_stop_app()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
