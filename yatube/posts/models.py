from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    """Класс групп"""

    title = models.CharField('Имя', max_length=150)
    slug = models.SlugField('Адрес')
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    """Класс постов"""

    text = models.TextField()
    pub_date = models.DateTimeField("date_published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, related_name="groups")
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.text


class Comments(models.Model):
    """Класс комментариев"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created = models.DateTimeField("Дата комментария", auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.text}"


class Follow(models.Model):
    """Класс таблицы подписок на авторов постов"""

    # ссылка на объект пользователя, который подписывается
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    # ссылка на объект пользователя, на которого подписываются
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"{self.user} подписан на {self.author}"
