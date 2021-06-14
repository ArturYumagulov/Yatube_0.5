from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from posts.models import User, Post  # noqa


class PostsApiTest(APITestCase):

    def setUp(self) -> None:

        self.is_authenticated = User.objects.create_user(
            username="sarah",
            email="connor.s@skynet.com",
            password="Zico123456789")

        self.post = Post.objects.create(
            text="You're talking about things I haven't done yet in the past tense. It's driving me crazy!",
            author=self.is_authenticated)

    def test_posts(self):
        #  проверка получения токена
        token_response = self.client.post('/api/v1/token-auth/',
                                    data={'username': self.is_authenticated.username,
                                          'password': "Zico123456789"},
                                    format='json')
        self.assertTrue('token' in token_response.json().keys()), "Токен не получен"

        #  проверка выдачи постов
        token = Token.objects.get(user__username='sarah')  # noqa
        client = APIClient(HTTP_AUTHORIZATION='Token ' + token.key)
        headers = {'Authorization': "Token " + token.key}
        response = client.get('/api/v1/posts/', headers={'Authorization': "Token " + token.key})
        self.assertEqual(response.json()[0]['text'], self.post.text), "Пост не соответствует"

        #  проверка добавления поста
        test_post = Post.objects.create(text='test_post', author=self.is_authenticated)
        add_post = client.post('/api/v1/posts/', data={'text': test_post.text, 'author': test_post.author.pk},
                               format='json', headers=headers)
        self.assertEqual(add_post.json()['text'], test_post.text), "пост не добавлен"

        #  редактирование поста
        #  Patch
        edit_post = client.patch(f'/api/v1/posts/{test_post.pk}/',
                                 data={'text': "edit_post", 'author': test_post.author.pk},
                                 format='json', headers=headers)
        self.assertEqual(edit_post.json()['text'], 'edit_post'), "редактирование через patch не работает"

        #  put
        edit_post = client.put(f'/api/v1/posts/{test_post.pk}/',
                               data={'text': "edit_post_put", 'author': test_post.author.pk},
                               format='json', headers=headers)
        self.assertEqual(edit_post.json()['text'], 'edit_post_put'), "редактирование через put не работает"

