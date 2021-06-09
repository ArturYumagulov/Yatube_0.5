from django import forms

from .models import Post, Group, Comments, Follow


class PostForm(forms.ModelForm):
    """Форма добавления поста"""

    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Группа", required=False)
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ("group", "text", "image",)


class CommentsAddForm(forms.ModelForm):
    """Форма добавления комментария"""

    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comments
        fields = ('text',)


class FollowForm(forms.ModelForm):
    """"""
    class Meta:
        model = Follow
        labels = {
            'user': 'пользователь подписывается на',
            'author': 'Автор данной записи'
        }
        help_texts = {
            'user': 'Вы подписываетесь на',
            'author': 'Автор данной записи'
        }
        fields = ['user']
