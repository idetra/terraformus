from allauth.account.forms import SignupForm, ResetPasswordForm
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible


# User related forms----------------------------------------------------------------------------------------------------


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # user = super(CustomSignupForm, self).save(request)
        user.save()
        return user

    # def save(self, request, user):
    #     user = super(CustomSignupForm, self).save(request)
    #     return user


# class ProfileForm(forms.ModelForm):
#     biography = forms.CharField(
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
#         required=False
#     )
#
#     class Meta:
#         model = Profile
#         fields = ['biography']


class UserUpdateForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-name-width'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-name-width'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-name-width'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class CustomResetPasswordForm(ResetPasswordForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)