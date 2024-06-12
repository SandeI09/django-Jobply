import re
from django import forms
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField()
    last_name = forms.CharField()
    class Meta:
        model = User
        fields = ["email", "first_name", "middle_name", "last_name"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data["password1"] != cleaned_data["password2"]:
            raise forms.ValidationError("Password didn't match!")
        return super().clean()
    
    # def clean_password1(self):    # validate_password1 for serializers(api)
    #     password1 = self.cleaned_data["password1"]
    #     if(len(password1)<8):
    #         raise forms.ValidationError("Password must be 8 characters long!")
    #     if not re.search(r'\d', password1) or not re.search(r'[A-Za-z]', password1):
    #         raise forms.ValidationError("Password must contain both numbers and characters.")
    #     return password1
    
class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'phone', 'address', 'resume', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = False
        self.fields['profile_picture'].required = False
        self.fields['address'].required = False
        self.fields['resume'].required = False
        self.fields['bio'].required = False