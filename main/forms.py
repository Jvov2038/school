from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from phonenumber_field.formfields import PhoneNumberField
from userprofile.models import UserProfile, SchoolClass, School, District
from .models import Subscriber
from dal import autocomplete


class UserProfileForm(forms.ModelForm):
    last_name = forms.CharField(
        max_length=30,
        required=False,
        label='Фамилия',
        widget=forms.TextInput(attrs={"placeholder": "Фамилия", "class": "newsletter_input"})
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        label='Имя',
        widget=forms.TextInput(attrs={"placeholder": "Имя", "class": "newsletter_input"})
    )
    patronymic = forms.CharField(
        max_length=30,
        required=False,
        label='Отчество',
        widget=forms.TextInput(attrs={"placeholder": "Отчество", "class": "newsletter_input"})
    )
    address = forms.CharField(
        max_length=30,
        required=False,
        label='Адрес',
        widget=forms.TextInput(attrs={"placeholder": "Адрес", "class": "newsletter_input"})
    )
    phone_number = PhoneNumberField(
        region="RU",
        label='Номер телефона',
        widget=forms.TextInput(attrs={"placeholder": "Номер телефона", "class": "newsletter_input"})
    )

    class Meta:
        model = UserProfile
        fields = ['last_name', 'first_name', 'patronymic', 'gender', 'address', 'phone_number']


class PersonalAreaForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Username", "autocomplete": "username", "class": "newsletter_input"})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "Email", "autocomplete": "email", "class": "newsletter_input"})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        label='Фамилия',
        widget=forms.TextInput(attrs={"placeholder": "Фамилия", "class": "newsletter_input"})
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        label='Имя',
        widget=forms.TextInput(attrs={"placeholder": "Имя", "class": "newsletter_input"})
    )
    patronymic = forms.CharField(
        max_length=30,
        required=False,
        label='Отчество',
        widget=forms.TextInput(attrs={"placeholder": "Отчество", "class": "newsletter_input"})
    )
    address = forms.CharField(
        max_length=30,
        required=False,
        label='Адрес',
        widget=forms.TextInput(attrs={"placeholder": "Адрес", "class": "newsletter_input"})
    )
    phone_number = PhoneNumberField(
        region="RU",
        label='Номер телефона',
        widget=forms.TextInput(attrs={"placeholder": "Номер телефона", "class": "newsletter_input"})
    )
    merit = forms.CharField(
        max_length=30,
        required=False,
        label='О себе',
        widget=forms.Textarea(attrs={"placeholder": "О себе", "class": "newsletter_input", "rows": 3})
    )
    school_class = forms.ModelChoiceField(
        queryset=SchoolClass.objects.all(),
        label='Класс',
        required=False,
        widget=forms.Select(attrs={'class': 'newsletter_input'})
    )
    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        label='Школа',
        required=False,
        widget=forms.Select(attrs={'class': 'newsletter_input'})
    )
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        label='Район',
        required=False,
        widget=forms.Select(attrs={'class': 'newsletter_input'})
    )

    class Meta:
        model = UserProfile
        fields = [
            'image', 'username', 'email', 'last_name', 'first_name', 'patronymic',
            'address', 'phone_number', 'birth', 'school_class', 'school', 'district', 'merit'
        ]
        widgets = {
            'birth': AdminDateWidget(attrs={'type': 'text', 'class': 'newsletter_input datepicker'}),
            'school': autocomplete.ModelSelect2(url='school-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = user.username
        self.fields['email'].initial = user.email
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['patronymic'].initial = user.userprofile.patronymic
        self.fields['address'].initial = user.userprofile.address
        self.fields['phone_number'].initial = user.userprofile.phone_number
        self.fields['birth'].initial = user.userprofile.birth
        self.fields['school_class'].initial = user.userprofile.school_class
        self.fields['school'].initial = user.userprofile.school
        self.fields['district'].initial = user.userprofile.district
        self.fields['merit'].initial = user.userprofile.merit
        self.fields['image'].initial = user.userprofile.image

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = self.instance.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            user_profile.save()
            self.save_m2m()
        return user_profile


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'newsletter_input', 'placeholder': 'Введите ваш email'})
        }


class UnsubscriberForm(forms.Form):
    email = forms.EmailField(
        label="Ваш email",
        widget=forms.EmailInput(attrs={
            "placeholder": "Email address",
            "autocomplete": "email",
            "class": "form-control"
        })
    )
