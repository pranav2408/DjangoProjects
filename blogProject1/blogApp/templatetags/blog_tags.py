from blogApp.models import Post
from django import template
from django.db.models import Count

register = template.Library()


@register.simple_tag(name='count')  # assign name o a tag. If not assigned, name is function name
def total_posts():
    return Post.objects.count()


@register.inclusion_tag('blogApp/latest.html', name='latest')
def show_latest_posts(count=1):  # defult 3 if not provided
    latest_post = Post.objects.order_by('-publish')[:count]  # will give latest 3 posts
    return {'latest_posts': latest_post}  # this data will be automatically sent to latest.html


@register.simple_tag(name='top_commented')
def get_most_commented_posts(count=1):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[
           :count]  # adds ne column total_comments and saves total comments for each posts in it . user related_name check it
