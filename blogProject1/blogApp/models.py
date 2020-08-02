from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class CustomManager(models.Manager):
    def get_queryset(self):
        print('inside custom manager')
        return super().get_queryset().filter(status='published')  # custom manager to return only published status


# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))  # tuple of tuples for dropdown choices
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=264, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)  # at what time object got created
    updated = models.DateTimeField(auto_now=True)  # at what time save method called
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = CustomManager()  # register custom manager
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)  # order by publish descending

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.status, self.publish.year, self.publish.strftime('%m'), self.publish.strftime('%d'),
                             self.slug])


# model for comments section
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Commented by {} on {}'.format(self.name, self.updated)
