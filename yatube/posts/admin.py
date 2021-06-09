from django.contrib import admin

from .models import Post, Group, Follow


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'image', 'text', 'pub_date', 'author', 'group',)
    search_fields = ('text',)
    list_filter = ('pub_date', 'group',)
    empty_value_display = "-пусто-"


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
# admin.site.register(Follow)
