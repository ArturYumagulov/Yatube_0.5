from django.test import TestCase, Client
from django.urls import reverse

from .models import User, Post


class ProfileTest(TestCase):
    """Тестовый класс"""

    def setUp(self):
        """Создание юзера и записи"""

        self.client = Client()
        self.is_authenticated = User.objects.create_user(
            username="sarah",
            email="connor.s@skynet.com",
            password="Zico123456789")

        self.post = Post.objects.create(
            text="You're talking about things I haven't done yet in the past tense. It's driving me crazy!",
            author=self.is_authenticated)

    def test_profile(self):
        self.client.force_login(self.is_authenticated)
        response = self.client.post('/new/', {'text': 'тест тест'}, follow=True)
        p = Post.objects.get(text='тест тест')
        self.assertEqual(response.context['post'], p), "Пост не создан"
        for url in ('', '/profile/sarah/', f'/profile/sarah/{p.pk}/'):
            response = self.client.get(url)
            self.assertContains(response, p.text), "Ошибка в адресах"
        res = self.client.post(f'/profile/sarah/{p.pk}/edit/',
                               {'text': 'edit_post', 'username': 'sarah', 'post_id': p.pk},
                               follow=True)
        edit_post = Post.objects.get(text="edit_post")
        self.assertContains(res, edit_post), "Пост не изменен"

    def test_edit_post_no_login(self):
        edited = self.client.post(f'/profile/sarah/{self.post.pk}/edit/',
                                  {'text': 'edit_post', 'username': 'test', 'post_id': self.post.pk}, follow=True)
        self.assertRedirects(edited, f"/auth/login/?next=/profile/sarah/{self.post.pk}/edit/")

