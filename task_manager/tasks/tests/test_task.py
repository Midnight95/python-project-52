from django.urls import reverse_lazy
from task_manager.users.models import User
from task_manager.tasks.models import Task
from .task_setup import TaskTestCase


class TestTaskCRUD(TaskTestCase):
    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_task_authorized(self):
        response = self.client.get(reverse_lazy('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/tasks.html')

    def test_task_unathorized(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('tasks'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('home'))

    def test_task_creation(self):
        data = self.task_test_data['valid']
        response = self.client.post(
            reverse_lazy('task_create'),
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertEqual(len(Task.objects.all()), 4)

    def test_task_creation_unautorized(self):
        self.client.logout()
        data = self.task_test_data['valid']
        response = self.client.post(
            reverse_lazy('task_create'),
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('home'))
        self.assertEqual(len(Task.objects.all()), 3)

    def test_task_creation_non_unique(self):
        data = self.task_test_data['invalid_non_unique']
        response = self.client.post(
            reverse_lazy('task_create'),
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Task.objects.all()), 3)

    def test_task_creation_empy_name(self):
        data = self.task_test_data['invalid_empty_name']
        response = self.client.post(
            reverse_lazy('task_create'),
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Task.objects.all()), 3)

    def test_task_update(self):
        data = self.task_test_data['valid']
        response = self.client.post(
            reverse_lazy('task_update', kwargs={'pk': 1}),
            data=data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['name'])

    def test_task_deletion(self):
        response = self.client.post(
            reverse_lazy('task_delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertEqual(len(Task.objects.all()), 2)
