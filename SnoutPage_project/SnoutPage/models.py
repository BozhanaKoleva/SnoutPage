from django.db import models

from django.utils import timezone

# A draft for models

class Category(models.Model):
    name = models.CharField(max_length=18, unique=True) 
    class Meta:
        verbose_name_plural = 'Categories'
        def __str__(self):
            return self.name

class Post(models.Model):
    category = models.ForeignKey(Category) 
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=300, blank=True)
    comments = models.CharField(max_length=300, default=0)
    tags = models.CharField(max_length=30, blank=True)
    picture = models.ImageField(upload_to='post_images', blank=True) 
    likes = models.IntegerField(default=0) 
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title



from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images',blank=True)

    def __str__(self):
        return self.user.username


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

