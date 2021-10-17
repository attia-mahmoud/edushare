from django import forms
from .models import User, Profile, Posts

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'uni', 'profile_pic')

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('post_type', 'title', 'desc', 'doc', 'video', 'subject', 'university', 'level')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['username', 'email']
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=['profile_pic','bio']