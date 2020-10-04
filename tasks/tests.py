from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from knox.models import AuthToken


class CreateTaskTestCase(APITestCase):

    task_create_url = reverse('task-create')

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token = AuthToken.objects.create(user=self.user)[1]
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_task_create_success(self):
        data = {
            'name': 'Listen to The Beatles',
            'description': 'Abbey Road is a great album'
        }
        response = self.client.post(self.task_create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        task = response.data['task']
        self.assertEqual(task['name'], data['name'])
        self.assertEqual(task['description'], data['description'])
        self.assertEqual(task['status'], 'New')
        self.assertEqual(task['scheduled_on'], None)
        self.assertEqual(task['creator']['id'], self.user.id)
        self.assertEqual(task['creator']['username'], self.user.username)

    def test_task_create_fail_missing_description(self):
        data = {
            'name': 'Hi Axl!'
        }
        response = self.client.post(self.task_create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_task_create_fail_missing_name(self):
        data = {
            'description': 'Hi Dave!'
        }
        response = self.client.post(self.task_create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RetrieveAllTasksTestCase(APITestCase):

    retrieve_all_tasks_url = reverse('tasks-all')
    task_create_url = reverse('task-create')

    mock_tasks = [
        {'name': 'test1', 'description': 'test1'},
        {'name': 'test2', 'description': 'test2'},
        {'name': 'test3', 'description': 'test3'},
    ]

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token = AuthToken.objects.create(user=self.user)[1]
        self.api_authentication()
        self.create_mock_tasks()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def create_mock_tasks(self):
        for mock_task in self.mock_tasks:
            response = self.client.post(self.task_create_url, data=mock_task)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_all_tasks_success(self):
        response = self.client.get(self.retrieve_all_tasks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.mock_tasks))
        for entry in response.data:
            self.assertEqual(entry['creator']['id'], self.user.id)

    def test_retrieve_all_tasks_fail(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.retrieve_all_tasks_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RetrieveUpdateTaskTestCase(APITestCase):

    task_create_url = reverse('task-create')

    mock_task = {
        'name': 'Initial name',
        'description': 'Initial description'
    }

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token = AuthToken.objects.create(user=self.user)[1]
        self.api_authentication()
        self.create_mock_task()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def create_mock_task(self):
        response = self.client.post(self.task_create_url, data=self.mock_task)
        self.task = response.data['task']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_task_success(self):
        response = self.client.get(reverse('task-retrieve-update', kwargs={'pk': self.task['id']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task = response.data
        self.assertEqual(task['name'], self.task['name'])
        self.assertEqual(task['description'], self.task['description'])
        self.assertEqual(task['status'], self.task['status'])
        self.assertEqual(task['scheduled_on'], self.task['scheduled_on'])
        self.assertEqual(task['creator']['id'], self.task['creator']['id'])
        self.assertEqual(task['creator']['username'], self.task['creator']['username'])

    def test_retrieve_task_fail(self):
        response = self.client.get(reverse('task-retrieve-update', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_fail(self):
        data = {}
        response = self.client.put(reverse('task-retrieve-update', kwargs={'pk': self.task['id']}), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_task_success(self):
        data = {
            'name': 'New name',
            'description': 'New description',
            'status': 'In-Progress'
        }
        response = self.client.put(reverse('task-retrieve-update', kwargs={'pk': self.task['id']}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['status'], data['status'])

    def test_update_task_with_status_scheduled_fail(self):
        data = {
            'status': 'Scheduled',
        }
        response = self.client.put(reverse('task-retrieve-update', kwargs={'pk': self.task['id']}), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_task_with_status_scheduled_success(self):
        data = {
            'status': 'Scheduled',
            'scheduled_on': '2020-01-01T03:03:33Z'
        }
        response = self.client.put(reverse('task-retrieve-update', kwargs={'pk': self.task['id']}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], data['status'])
        self.assertEqual(response.data['scheduled_on'], data['scheduled_on'])


class ChangesTestCase(APITestCase):
    task_create_url = reverse('task-create')

    mock_task = {
        'name': 'Initial name',
        'description': 'Initial description'
    }

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token = AuthToken.objects.create(user=self.user)[1]
        self.api_authentication()
        self.create_mock_task()
        self.do_some_changes()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def create_mock_task(self):
        response = self.client.post(self.task_create_url, data=self.mock_task)
        self.task = response.data['task']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def do_some_changes(self):
        data = {
            'name': 'New name',
            'description': 'New Description'
        }
        response = self.client.put(reverse('task-retrieve-update', kwargs={'pk': self.task['id']}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])

        data = {
            'status': 'Scheduled',
            'scheduled_on': '2020-01-01T03:03:33Z'
        }
        response = self.client.put(reverse('task-retrieve-update', kwargs={'pk': self.task['id']}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], data['status'])
        self.assertEqual(response.data['scheduled_on'], data['scheduled_on'])

    def test_tasks_changes(self):
        response = self.client.get(reverse('task-changes', kwargs={'pk': self.task['id']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Creation and two updates
