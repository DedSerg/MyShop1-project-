from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Order



from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'address', 'phone_number', 'email', 'additional_info']
        labels = {
            'full_name': 'Полное имя',
            'address': 'Адрес',
            'phone_number': 'Телефон',
            'email': 'Электронная почта',
            'additional_info': 'Дополнительная информация',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше полное имя'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш адрес'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш телефон'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'}),
            'additional_info': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Дополнительная информация', 'rows': 3}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'date_of_birth', 'phone_number', 'email', 'last_name', 'first_name']