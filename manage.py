#!/usr/bin/env python
"""
Утилита командной строки Django для административных задач.

Этот скрипт служит точкой входа для выполнения команд Django, таких как запуск сервера разработки,
миграции базы данных и другие административные задачи.

Перед выполнением команд устанавливает переменную окружения `DJANGO_SETTINGS_MODULE`,
указывающую на файл настроек проекта.
"""

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
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
