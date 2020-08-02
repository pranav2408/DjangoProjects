from django.contrib import admin
from blogApp.models import Post, Comment


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'body', 'publish', 'created', 'updated', 'status')
    prepopulated_fields = {'slug': ('title',)}  # to prepopulate slug field based on title
    list_filter = ('status', 'author', 'created', 'publish')  # to add filter based on mentioned fields
    search_fields = ('title', 'body')  # to add search field, will search in title and body
    raw_id_fields = ('author',)  # to accept id instead of selecting author from dropdown
    date_hierarchy = 'publish'  # to add navbar based on dates
    ordering = ('status', 'publish')  # to order posts based on given fields


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created',  'updated', 'body', 'post', 'active']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
