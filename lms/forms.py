from django import forms

from lms.models import User, Lessons, Category, Test
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class LoginUserForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def save(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        return email, password


class CreateLessonsForm(forms.ModelForm):
    class Meta:
        model = Lessons
        fields = ('title', 'description', 'link', 'file_upload', 'image', 'video', 'category')


class CreateClassroomForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class CreateTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('name', 'description', 'category')