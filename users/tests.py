from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models import Task

User = get_user_model()


class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user-list')  # Эндпоинт для создания пользователя
        self.registration_url = reverse('user-registration')
        self.token_url = reverse('token_obtain_pair')  # Эндпоинт для получения токена (по умолчанию /api/token/)

        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }

    def test_user_registration(self):
        # Данные для регистрации пользователя
        registration_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
            # Другие необходимые данные для регистрации
        }
        # Отправляем запрос на регистрацию пользователя
        response = self.client.post(self.registration_url, registration_data)
        # Проверяем, что запрос был успешным
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        # Сначала регистрируем пользователя с email, т.к. используется кастомная модель пользователя
        User.objects.create_user(email="testuser@example.com", password="testpassword123")
        # Определяем данные для входа, используя email вместо username
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        # Затем пытаемся получить JWT токен
        response = self.client.post(self.token_url, self.user_data)
        # Проверяем, что запрос был успешным
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что в ответе присутствует токен доступа
        self.assertIn("access", response.data)


class TaskCRUDTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.client = APIClient()
        self.user = User.objects.create_user(email="testuser@example.com", password="testpassword123")

        # Получаем токен
        self.token_url = reverse('token_obtain_pair')
        response = self.client.post(self.token_url, {"email": "testuser@example.com", "password": "testpassword123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Ошибка при получении токена")
        self.access_token = response.data.get("access")

        # Добавляем токен к заголовкам
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Создаем URL для задач
        self.tasks_url = reverse('task-list')

    def test_create_task(self):
        task_data = {
            "title": "Test Task",
            "description": "Test Task Description",
            "status": "новая"
        }
        response = self.client.post(self.tasks_url, task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], task_data["title"])

    def test_get_task_list(self):
        # Создаем несколько задач
        Task.objects.create(title="Test Task 1", description="Description 1", status="новая", user=self.user)
        Task.objects.create(title="Test Task 2", description="Description 2", status="в процессе", user=self.user)

        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_task(self):
        # Создаем задачу
        task = Task.objects.create(title="Test Task", description="Description", status="новая", user=self.user)
        update_url = reverse('task-detail', args=[task.id])

        updated_data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "status": "завершена"
        }

        response = self.client.put(update_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], updated_data["title"])

    def test_delete_task(self):
        # Создаем задачу
        task = Task.objects.create(title="Test Task", description="Description", status="новая", user=self.user)
        delete_url = reverse('task-detail', args=[task.id])

        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
