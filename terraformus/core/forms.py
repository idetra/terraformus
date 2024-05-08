from allauth.account.forms import SignupForm, ResetPasswordForm
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible

from terraformus.core.models import Solution, Profile, ExternalAsset, LifeCycle, LifeCycleInput, LifeCycleWaste


# SOLUTIONS & STRATEGIES -----------------------------------------------------------------------------------------------


class SolutionForm(forms.ModelForm):
    derives_from = forms.CharField(required=False)

    class Meta:
        model = Solution
        fields = '__all__'
        exclude = ['user', 'depends_on', 'slug', 'banned']

    def __init__(self, *args, **kwargs):
        super(SolutionForm, self).__init__(*args, **kwargs)
        if self.instance.pk and self.instance.derives_from:
            self.initial['derives_from'] = self.instance.derives_from.title

    def clean_derives_from(self):
        derives_from_title = self.cleaned_data['derives_from']
        if derives_from_title:
            try:
                derives_from_instance = Solution.objects.get(title=derives_from_title)
            except Solution.DoesNotExist:
                raise forms.ValidationError("Solution with this title does not exist")
            return derives_from_instance
        return None


class DependsOnForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control custom-reference-width',
               'placeholder': 'Exact match (case sensitive)'}),
        max_length=255, required=False)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            try:
                return Solution.objects.get(title=title)
            except Solution.DoesNotExist:
                raise ValidationError('No Solution with this title exists')
        return None


# EXTERNAL ASSETS & LIFE CYCLES ----------------------------------------------------------------------------------------


class ExternalAssetForm(forms.ModelForm):
    class Meta:
        model = ExternalAsset
        fields = '__all__'
        exclude = ['user', 'solution', 'strategy']


class LifeCycleForm(forms.ModelForm):
    class Meta:
        model = LifeCycle
        fields = '__all__'
        exclude = ['solution',]


class InLineLifeCycleInputForm(forms.ModelForm):
    class Meta:
        model = LifeCycleInput
        fields = '__all__'


class InLineLifeCycleWasteForm(forms.ModelForm):
    class Meta:
        model = LifeCycleWaste
        fields = '__all__'


# User related forms----------------------------------------------------------------------------------------------------


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class ProfileForm(forms.ModelForm):
    biography = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ['biography']


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