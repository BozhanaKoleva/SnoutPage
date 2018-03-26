from django import forms
from django.contrib.auth.models import User
from SnoutPage.models import UserProfile, Pet, Comment,  Post, PostLike, AdditonalUserData, Follow, ImageTest #Page
from SnoutPage.types import *

from django.contrib.auth.forms import UserChangeForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget =forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget =forms.PasswordInput(),required =True)
    email = forms.EmailField(required = True)
    username =forms.CharField(required=True)
    class Meta:
        model = UserProfile
        fields = ('Userpicture',)

class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ('followed',)

class PetForm(forms.ModelForm):
##   category = forms.ChoiceField(choices = TYPES, label="", initial='', widget=forms.Select(), )
##   name = forms.CharField(max_length=128)
##   picture = forms.ImageField
##   description = forms.CharField(max_length=600)
   class Meta:
    model = Pet
    fields = ('category', 'name','description', 'picture')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('description',)

##class PageForm(forms.ModelForm):
##    title = forms.CharField(max_length=128,
##    help_text="Please enter the title of the page.")
##    url = forms.URLField(max_length=200,
##    help_text="Please enter the URL of the page.")
##    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
##
##    class Meta:
##        model = Page
##        fields = ('title', 'url', 'views')
##
##    def clean(self):
##        cleaned_data = self.cleaned_data
##        url = cleaned_data.get('url')
##
##        if url and not url.startswith('http://'):
##            url = 'http://' + url
##            cleaned_data['url'] = url
##            return cleaned_data

class PostForm(forms.ModelForm):
##    title = forms.CharField(max_length=128,
##    help_text="Please enter the title of the post.")
##    description = forms.CharField(max_length=300,
##    help_text="Please enter the description of the post.")
##    tags = forms.CharField (max_length=30,
##    help_text="Add a tag.")
##    picture = forms.ImageField()
##    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    class Meta:
        model = Post
        fields = ('title', 'description', 'tag', 'picture','image')


class PostLikeForm(forms.ModelForm):
    class Meta:
        model = PostLike
        fields = ()

class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email','first_name','last_name')
        exclude=('password',)
    def __init__self(self, *args, **kwargs):
        super(EditUserForm,self).__init__(*args, **kwargs)
        self.fields['password'].help_text=None

class EditOtherDetails(forms.ModelForm):
    class Meta:
        model = AdditonalUserData
        fields = ('description','picture')


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageTest
        fields = ('description','image')
