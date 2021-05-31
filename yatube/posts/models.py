from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Имя', max_length=150)
    slug = models.SlugField('Адрес')
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date_published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, related_name="groups")

    def __str__(self):
        return self.text
