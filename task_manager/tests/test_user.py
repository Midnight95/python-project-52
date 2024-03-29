from django.test import TestCase
from django.urls import reverse_lazy
from task_manager.user.models import User


class TestIndex(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse_lazy('home'))

    def test_index_view(self):

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, template_name='index.html')
        self.assertContains(self.response, 'Task Manager')

        self.assertContains(self.response, '/users/')
        self.assertContains(self.response, '/login/')
        self.assertNotContains(self.response, '/logout/')


class TestUserCreation(TestCase):
    def setUp(self):
        self.data = {
            'email': 'test@email.com',
            'first_name': 'User',
            'last_name': 'Uservocich',
            'username': 'user',
            'password1': 'jgoi34^@dFF',
            'password2': 'jgoi34^@dFF'
            }

    def test_user_creation_url(self):
        response = self.client.get(reverse_lazy('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='forms/form.html')

    def test_user_creation(self):
        response = self.client.post(
                reverse_lazy('user_create'), data=self.data
                )
        self.assertRedirects(response, expected_url=reverse_lazy('login'))
        user = User.objects.get(username="user")
        self.assertTrue(user.is_active)


class TestUser(TestCase):
    def setUp(self):
        self.user_credentials = {
            'username': 'login_user',
            'password': 'lup@ssW@rd'
        }
        self.user = User.objects.create_user(**self.user_credentials)

    def test_user_login_url(self):
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='forms/form.html')

    def test_login(self):
        response = self.client.post(
                reverse_lazy('login'), data=self.user_credentials, follow=True
                )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse_lazy('home'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('home'))
        self.assertContains(response, 'logout')

        response = self.client.post(reverse_lazy('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'logout')
