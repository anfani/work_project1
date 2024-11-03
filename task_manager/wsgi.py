"""
WSGI конфигурация для проекта task_manager.

Этот модуль предоставляет объект WSGI-приложения на уровне модуля под именем "application".

Для получения дополнительной информации об этом файле, см. ссылку:
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Установка модуля настроек проекта по умолчанию.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')

# Получение WSGI-приложения для запуска.
application = get_wsgi_application()
