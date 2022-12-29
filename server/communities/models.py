from django.db import models

from core.mixins import BaseModel


class Post(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    backdrop_image = models.URLField(null=True, blank=True)
    hits = models.PositiveIntegerField(default=1)
    tags = models.ManyToManyField('communities.PostTag', blank=True, related_name='posts')
    likes = models.ManyToManyField('accounts.Profile', blank=True, related_name='post_likes')


class PostImage(models.Model):
    image = models.ImageField(upload_to='community/%Y-%m')


class PostTag(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Comment(BaseModel):
    post = models.ForeignKey('communities.Post', on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    replies = models.ManyToManyField('self')
    comment = models.TextField()
