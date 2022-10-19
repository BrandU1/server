from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint, Deferrable

from core.mixins import BaseModel


class Post(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    backdrop_image = models.ImageField(upload_to='community/backdrop/%Y-%m', null=True)
    comments = models.ManyToManyField('accounts.Profile', through='communities.Comment',
                                      through_fields=('post', 'profile'), related_name='+')
    hits = models.PositiveIntegerField(default=1)

    @property
    def contents(self):
        return self.content_set.all().order_by('-priority')


class Content(BaseModel):
    post = models.ForeignKey('communities.Post', on_delete=models.CASCADE)
    priority = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    description = models.TextField(null=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['post', 'priority'], name='unique_content_priority',
                             deferrable=Deferrable.DEFERRED),
        ]


class ContentImage(models.Model):
    content = models.ForeignKey('communities.Content', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='community/%Y-%m')
    tag = models.ForeignKey('communities.Tag', on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Comment(BaseModel):
    post = models.ForeignKey('communities.Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    replies = models.ManyToManyField('self')
    comment = models.CharField(max_length=500)


class Review(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='community_review_set')
