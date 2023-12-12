from django import forms
from django.forms import modelformset_factory
from django_countries.fields import CountryField
from lms.models import User, Lessons, Classrooms, Test, Question, Options, ProfileUser
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = ('phone_number', 'address', 'city', 'country', 'birth_date', 'photo', 'bio')

        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CreateUserAndProfileForm(UserCreationForm, ProfileUserForm):
    country = CountryField().formfield()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.update(ProfileUserForm(self.data).fields)


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
        fields = ('title', 'description',)

    def __init__(self, *args, **kwargs):
        super(CreateLessonsForm, self).__init__(*args, **kwargs)
        self.fields['users'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)


class CreateClassroomForm(forms.ModelForm):
    class Meta:
        model = Classrooms
        fields = ('name',)


class CreateTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('name', 'description', 'category', 'users',)

    def __init__(self, *args, **kwargs):
        super(CreateTestForm, self).__init__(*args, **kwargs)
        self.fields['users'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('name', 'points')


class CreateOptionForm(forms.ModelForm):
    class Meta:
        model = Options
        fields = ['text', 'is_correct']


CreateOptionFormSet = modelformset_factory(
    Options,
    form=CreateOptionForm,
    extra=5,
)
