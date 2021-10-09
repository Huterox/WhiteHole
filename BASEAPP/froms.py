from django import forms
from .models import UserPic

class UserPicForm(forms.ModelForm):
    class Meta:
        model = UserPic
        fields = ['userpic']
