from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Order
from django.core.files.images import get_image_dimensions

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')
    first_name = forms.CharField(max_length=150, required=True, label='Имя')
    last_name = forms.CharField(max_length=150, required=True, label='Фамилия')
    date_of_birth = forms.DateField(required=False, widget=forms.SelectDateWidget(years=range(1900, 2025)), label='Дата рождения')
    phone_number = forms.CharField(max_length=15, required=False, label='Номер телефона')
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'date_of_birth', 'phone_number']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Храните пароль в зашифрованном виде
        if commit:
            user.save()
            # Создание UserProfile после сохранения пользователя
            UserProfile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                phone_number=self.cleaned_data['phone_number']
            )
        return user

class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['avatar', 'date_of_birth', 'phone_number', 'email', 'last_name', 'first_name']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            try:
                w, h = get_image_dimensions(avatar)

                # Validate dimensions
                max_width = max_height = 100
                if w > max_width or h > max_height:
                    raise forms.ValidationError(
                        u'Пожалуйста, используйте изображение размером '
                         '%s x %s пикселей или меньше.' % (max_width, max_height))

                # Validate content type
                main, sub = avatar.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                    raise forms.ValidationError(u'Пожалуйста, используйте изображение в формате JPEG, '
                        'GIF или PNG.')

                # Validate file size
                if avatar.size > (20 * 1024):  # 20kB
                    raise forms.ValidationError(
                        u'Размер файла аватара не может превышать 20 кБ.')

            except AttributeError:
                # Handles case when we are updating the user profile
                # and do not supply a new avatar
                pass

        return avatar

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone_number', 'shipping_address']