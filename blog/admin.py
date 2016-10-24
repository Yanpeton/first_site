from django.contrib import admin
from blog.models import Article, Comment, UserProfile

admin.site.register([Article, Comment, UserProfile])

# Register your models here.
