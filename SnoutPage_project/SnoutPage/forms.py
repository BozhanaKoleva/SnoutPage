from django import forms
from django.contrib.auth.models import User
from SnoutPage.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget =forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
        
class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=default,
    help_text="Please enter the title of the post.")
    description = forms.CharField(max_length=300, blank=True,
    help_text="Please enter the description of the post.")
    tags = forms.CharField (max_length=30, blank=True,
    help_text="Add a tag.")
    picture = forms.ImageField(upload_to='post_images', blank=True)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    class Meta:
        model = Post
        fields = ('title', 'description', 'tags', 'picture',)

        
class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ('name', 'picture', 'description')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('description')

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=default,
    help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,
    help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
            return cleaned_data

    class Meta:
        model = Page
        fields = ('title', 'url', 'views')
