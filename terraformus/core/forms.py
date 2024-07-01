from allauth.account.forms import SignupForm, ResetPasswordForm
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible

from terraformus.core.models import Solution, Profile, ExternalAsset, LifeCycle, LifeCycleInput, LifeCycleWaste, \
    Strategy
from terraformus.core.services import aux_lists, choices


# SOLUTIONS & STRATEGIES -----------------------------------------------------------------------------------------------


class SolutionForm(forms.ModelForm):
    derives_from = forms.CharField(required=False, help_text=Solution._meta.get_field('derives_from').help_text)

    class Meta:
        model = Solution
        fields = '__all__'
        exclude = ['user', 'depends_on', 'slug', 'banned']

    def __init__(self, *args, **kwargs):
        super(SolutionForm, self).__init__(*args, **kwargs)
        if self.instance.pk and self.instance.derives_from:
            self.initial['derives_from'] = self.instance.derives_from.title

        # Defining the widgets here to preserve help_text from models

        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['subtitle'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['goal'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})

        self.fields['cost_type'].widget = forms.Select(choices=choices.cost_types.items(), attrs={'class': 'form-control'})
        self.fields['update'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        self.fields['upgrade'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        self.fields['scale_up'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})

        self.fields['derives_from'].widget = forms.TextInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'Solution title (exact match, case sensitive)'})

        for key in aux_lists.solutions_booleans:
            for field in aux_lists.solutions_booleans[key]:
                self.fields[field].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})

    def clean_derives_from(self):
        derives_from_title = self.cleaned_data['derives_from']
        if derives_from_title:
            try:
                derives_from_instance = Solution.objects.get(title=derives_from_title)
            except Solution.DoesNotExist:
                raise forms.ValidationError("Solution with this title does not exist")
            return derives_from_instance
        return None

    def clean_cost_type(self):
        cost_type = self.cleaned_data.get('cost_type')
        if cost_type is not None and cost_type < 0:
            raise forms.ValidationError('This field cannot be negative.')
        return cost_type


class DependsOnForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control custom-reference-width',
               'placeholder': 'Solution title (exact match, case sensitive)'}),
                max_length=255, required=False,
                help_text=mark_safe('<small class="form-text text-muted">If your solution depends on other solution(s), add it above - add more than one using the links below</small>'))

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            try:
                return Solution.objects.get(title=title)
            except Solution.DoesNotExist:
                raise ValidationError('No Solution with this title exists')
        return None


class StrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = ['title', 'goal', 'definitions']

    def __init__(self, *args, **kwargs):
        super(StrategyForm, self).__init__(*args, **kwargs)
        # Defining the widgets here to preserve help_text from models
        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['goal'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        self.fields['definitions'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})


class StrategySolutionForm(forms.Form):
    solution_title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control custom-reference-width',
               'placeholder': 'Exact match (case sensitive)'}),
        max_length=255, required=False)
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), required=False)

    def clean_solution_title(self):
        solution_title = self.cleaned_data.get('solution_title')
        if solution_title:
            try:
                return Solution.objects.get(title=solution_title)
            except Solution.DoesNotExist:
                raise ValidationError('No Solution with this title exists')
        return None



# EXTERNAL ASSETS & LIFE CYCLES ----------------------------------------------------------------------------------------


class ExternalAssetForm(forms.ModelForm):
    class Meta:
        model = ExternalAsset
        fields = '__all__'
        exclude = ['user', 'solution', 'strategy']

    def __init__(self, *args, **kwargs):
        super(ExternalAssetForm, self).__init__(*args, **kwargs)
        # Defining the widgets here to preserve help_text from models
        self.fields['type'].widget = forms.Select(choices=choices.external_asset.items(), attrs={'class': 'form-control'})
        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['url'].widget = forms.TextInput(attrs={'class': 'form-control'})


class LifeCycleForm(forms.ModelForm):
    class Meta:
        model = LifeCycle
        fields = '__all__'
        exclude = ['solution',]

    def __init__(self, *args, **kwargs):
        super(LifeCycleForm, self).__init__(*args, **kwargs)
        # Defining the widgets here to preserve help_text from models
        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['type'].widget = forms.Select(choices=choices.life_cycle_types.items(), attrs={'class': 'form-control'})
        self.fields['total_duration'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})


class InLineLifeCycleInputForm(forms.ModelForm):
    class Meta:
        model = LifeCycleInput
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(InLineLifeCycleInputForm, self).__init__(*args, **kwargs)
        # Defining the widgets here to preserve help_text from models
        self.fields['resource_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['resource_type'].widget = forms.Select(choices=choices.resource_types.items(), attrs={'class': 'form-control'})
        self.fields['unit'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['quantity'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['reference_cost'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['notes'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 7})


class InLineLifeCycleWasteForm(forms.ModelForm):
    class Meta:
        model = LifeCycleWaste
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(InLineLifeCycleWasteForm, self).__init__(*args, **kwargs)
        # Defining the widgets here to preserve help_text from models
        self.fields['waste_type'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['reusable'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['recyclable'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['cradle2cradle'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['unit'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['quantity'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['reference_cost'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['destination_method'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        self.fields['notes'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 2})


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