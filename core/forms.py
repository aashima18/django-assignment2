from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth.admin import UserAdmin
from .models import User,Assignment,Assignment_Request,Submission,Remark,Messages
from django.contrib.auth import get_user_model
User = get_user_model()

ROLE = (
      ('student', 'student'),
      ('teacher', 'teacher'),
  )

ROLES = (
      ('student', 'student'),
      
  )


STAR = (
      ('1star','1star'),
      ('2star','2star'),
      ('3star','3star'),
      ('4star','4star'),
      ('5star','5star'),
)  

class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    # check = forms.BooleanField(required = True,label='Terms and conditions')
    user_type = forms.ChoiceField(widget=forms.RadioSelect, choices=ROLE)
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username','email','user_type')
        

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('This email address is already registered.')
        return email

    
        


class PasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('password', 'confirm_password')
    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        min_length = 8
        if len(password) < min_length:
            msg = 'Password must be at least %s characters long.' %(str(min_length))
            self.add_error('password', msg)

        # check for digit
        if sum(c.isdigit() for c in password) < 1:
            msg = 'Password must contain at least 1 number.'
            self.add_error('password', msg)

        # check for uppercase letter
        if not any(c.isupper() for c in password):
            msg = 'Password must contain at least 1 uppercase letter.'
            self.add_error('password', msg)

        # check for lowercase letter
        if not any(c.islower() for c in password):
            msg = 'Password must contain at least 1 lowercase letter.'
            self.add_error('password', msg)

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class LoginForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'password')


class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True ,widget=forms.TextInput(attrs={'readonly':'readonly'}))
    Image = forms.ImageField(required=False)
    organization = forms.CharField(required=False)
    address = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','email','Image','organization','address')     



class AddStudentForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=True)
    user_type = forms.ChoiceField(widget=forms.RadioSelect, choices=ROLES)
    class Meta:
        model = User
        fields = ('username','email','user_type')
    


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('This email address is already registered.')
        return email        


class AssignmentForm(forms.ModelForm):
   
    description = forms.CharField(max_length=255)
    as_file = forms.FileField(required =True)
    class Meta:
        model = Assignment
        fields = ('description','as_file')        

class AssignmentForm1(forms.ModelForm):
   
    description = forms.CharField(max_length=255)
    submitted_file= forms.FileField(required =True)
    class Meta:
        model = Submission
        fields = ('description','submitted_file')

    def clean_date(self):
        Submitted_date = forms.DateTimeField(default=datetime.now(),blank=True)

        if Submitted_date > Assignment.objects.filter(submit_date=submit_date):
            raise forms.ValidationError('Times out')
        return Submitted_date





class AssignmenttForm(forms.ModelForm):
    request = forms.BooleanField(initial=True)
    class Meta:
        model=Assignment_Request    
        fields = ('request',)    



     


class ReviewForm(forms.ModelForm):
    rating= forms.ChoiceField(widget=forms.Select, choices=STAR)
    class Meta:
        model = Remark
        fields = ('rating',)        



class MessageForm(forms.ModelForm):
    msg = forms.CharField(widget=forms.TextInput(attrs={'class': 'arg','placeholder': 'Your message',}),label='say hii')
    class Meta:
        model = Messages
        fields =('msg',)

   