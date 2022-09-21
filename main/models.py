from os import link
from turtle import title
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.conf import settings


class Feed(models.Model):
    username = models.CharField	(max_length=20)
    name = models.CharField	(max_length=20)
    profileimg = models.TextField(default= "default_profile")
    content = models.TextField(null=True, blank=True)
    contentimg = models.TextField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)
    like_count = models.TextField(default= 0)
    like_or_not = models.BooleanField(default=True) # Whether the Login-User liked or not on a feed

    # Shared Feed
    shared_content_id = models.IntegerField(null=True, blank=True) # Shared feed id
    shared_feed_name = models.TextField(max_length=20, null=True, blank=True) # Shared feed's original writer
    shared_created_at = models.TextField(null=True, blank=True) # Shared feed's original created time

class Like(models.Model):
    username = models.CharField	(max_length=20) # User who liked
    feed = models.IntegerField(default=0) # The Feed that User liked
    is_like = models.BooleanField(default=True) # like = 1, non-like = 0

class Hide_Feed(models.Model):
    username = models.CharField	(max_length=20) 
    feed = models.IntegerField(default=0)

class Comment(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE) 
    username = models.CharField	(max_length=20, default="")   
    name = models.CharField	(max_length=20)
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment_like_count = models.TextField(default= 0)
    comment_like_or_not = models.BooleanField(default=False)

class Comment_Like(models.Model):
    username = models.CharField	(max_length=20)   
    comment = models.IntegerField(default=0)
    is_like = models.BooleanField(default=False)

class Comment_Comment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE) 
    username = models.CharField	(max_length=20, default="")     
    name = models.CharField	(max_length=20) 
    comment_comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment_comment_like_count = models.TextField(default= 0)
    comment_comment_like_or_not = models.BooleanField(default=False)

class User(AbstractBaseUser):
    username = models.CharField(max_length=24, unique=True)  # Username has to be one and only in database (unique)
    profileimg = models.TextField(default= "default_profile") # When a User signed up, Default profile is saved
    name = models.CharField(max_length=24)
    email = models.EmailField(default="")

    USERNAME_FIELD= 'username'

    objects = UserManager()

    class Meta:
        db_table = "User"

class News(models.Model):
    title = models.TextField(null=True, blank=True)
    picture = models.TextField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.title