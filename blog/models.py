from django.db import models
from django.contrib.auth.models import User
from blog.storage import OverwriteStorage


class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')
    real_last_login = models.DateTimeField(null=True)
    profile_image = models.FileField(upload_to='profile_image', storage=OverwriteStorage(), null=True,
                                     blank=True)
    GENDER_CHOICES = (
         ('female', 'Female'),
         ('male', 'Male'),
         )
    gender = models.CharField(null=True, blank=True, max_length=5,
                              choices=GENDER_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def is_completed(self):
        return True if self.profile_image and self.gender else False

    def __str__(self):
        return self.belong_to.username


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    watched_counts = models.IntegerField(default=0)
    got_counts = models.IntegerField(default=0)
    collectors = models.ManyToManyField(to=User, blank=True)
    TAG_CHOICES = (
            ('tech', 'Tech'),
            ('life', 'Life'),
            )
    tag = models.CharField(null=True, blank=True, max_length=5,
                           choices=TAG_CHOICES)
    published_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.tag + ':' + self.title


class Comment(models.Model):
    user = models.ForeignKey(to=User, related_name='user_comment', null=True,
                             blank=True)
    comment = models.TextField()
    belong_to = models.ForeignKey(to=Article, related_name='under_comments',
                                  null=True, blank=True)
    best_comment = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ':' + self.comment
