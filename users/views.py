"""
Модуль ViewSet'ов для API приложения Task Manager.

Содержит:
- UserViewSet: управление пользователями с поддержкой операций создания, получения,
  обновления и удаления. Ограничивает доступ только аутентифицированным пользователям.
- TaskViewSet: управление задачами с фильтрацией по текущему пользователю.
  Поддерживает создание, получение, обновление и удаление задач.

Особенности:
- Возвращает пустой QuerySet для Swagger-документации.
- Автоматически связывает задачи с текущим аутентифицированным пользователем при создании.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from tasks.models import Task
from users.models import User

from .serializers import TaskSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'put']

    def get_queryset(self):
        """
        Возвращает набор пользователей для отображения.
        Если запрос поступил от Swagger, возвращается пустой QuerySet.
        """
        if getattr(self, 'swagger_fake_view', False):
            return User.objects.none()  # Возвращаем пустой QuerySet для Swagger

        return User.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления задачами.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'put']

    def get_queryset(self):
        """
        Возвращает набор задач для текущего аутентифицированного пользователя.
        Если запрос поступил от Swagger, возвращается пустой QuerySet.
        """
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()  # Возвращаем пустой QuerySet для Swagger

        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Сохраняет новую задачу, назначенную текущему пользователю.
        """
        serializer.save(user=self.request.user)
