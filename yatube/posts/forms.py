from django import forms

from .models import Post, Group


class PostForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Группа", required=False)
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ("group", "text",)
