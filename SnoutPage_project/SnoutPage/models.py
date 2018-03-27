from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from SnoutPage.types import *


# A draft for models

class Category(models.Model):
   name = models.CharField(max_length=18, unique=True)
   class Meta:
       verbose_name_plural = 'Categories'
       def __str__(self):
           return self.name
##
##class Page(models.Model):
##    category = models.ForeignKey(Category)
##    title = models.CharField(max_length=128)
##    url = models.URLField()
##    views = models.IntegerField(default=0)
##
##    def __str__(self):
##        return self.title

class UserProfile(models.Model):

    user = models.OneToOneField(User)
    Userpicture = models.ImageField(upload_to='profile_images',blank=True)
    friends = models.IntegerField(default=0) ##not sure about this part
    description = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender = User)


class Pet(models.Model):
    slug = models.SlugField(unique=True, default=None)
    category = models.CharField(max_length=6, choices=TYPES, default="DOG")
    owner = models.ForeignKey(User, default=None)
    name = models.CharField(max_length=120, unique=True)
    picture = models.FileField(upload_to='pet_profile_images',blank=True)
    description = models.CharField(max_length=600, blank=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Pet, self).save(*args, **kwargs)

class Post(models.Model):
    slug = models.SlugField(unique=True, default=None)
    category = models.CharField(max_length=6, choices=TYPES, default="DOG")
    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=300, blank=True)
    tag = models.CharField(max_length=30, blank=True)
    picture = models.ImageField(upload_to='post_images', blank=True)
    pet = models.ForeignKey(Pet, default=None)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    image =models.FileField(null = True, blank = True,upload_to='post_images')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class PostLike(models.Model):
    user = models.ForeignKey(User)
    liked = models.BooleanField(default=False)
    post = models.ForeignKey(Post)
    def __str__(self):
        return self.user.username

class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=False)
    created_date = models.DateTimeField(default=timezone.now)
    ##likes = models.IntegerField(default=0)
    def __str__(self):
        return self.description


class AdditonalUserData(models.Model):
    user = models.ForeignKey(User)
    description = models.CharField(max_length=100, default="")
    picture = models.ImageField(upload_to='profile_images',blank=True)
    date = models.DateTimeField(default =timezone.now)

class ImageTest(models.Model):
    description = models.CharField(max_length=100, default ="")
    image =models.FileField(null = True, blank = True)

    class Meta:
        verbose_name_plural= "Images"

    def __str__(self):
        return self.description
    def save(self, *args, **kwargs):
        self.slug = slugify(self.description)
        super(ImageTest, self).save(*args, **kwargs)


class Follow (models.Model):
   followed = models.CharField(max_length=13, choices=FOLLOW, default="NOT_FOLLOWING")
   user = models.ForeignKey(User,  related_name='user')
   follower = models.ForeignKey(User,  related_name='follower')


# Create your models here.




##class Friend(models.Model):
##    users = models.ManyToManyField(User)
##    current_user = models.ForeignKey(User, related_name = 'owner',null=True)
##
##    @classmethod
##    def add_friend(cls, current_user, new_friend):
##        friend, created =cls.objects.get_or_create(current_user=current_user)
##        friend.users.add(new_friend)
##
##    @classmethod
##    def unfrienddef (cls, current_user, new_friend):
##        friend, created =cls.objects.get_or_create(current_user=current_user)
##        friend.users.remove(new_friend)
