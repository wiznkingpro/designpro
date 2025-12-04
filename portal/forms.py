from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DesignRequest, Category
from django.core.validators import RegexValidator
import re


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        label="ФИО",
        validators=[
            RegexValidator(
                regex=r'^[а-яА-ЯёЁ\s\-]+$',
                message="ФИО должно содержать только кириллические буквы, пробелы и дефисы."
            )
        ]
    )
    email = forms.EmailField(required=True, label="Email")
    agree_to_pd = forms.BooleanField(label="Согласие на обработку персональных данных")

    class Meta:
        model = User
        fields = ("username", "full_name", "email", "password1", "password2")
        labels = {
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Повтор пароля',
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("Логин обязателен.")
        # Только латинские буквы и дефисы; дефис не в начале/конце, без '--'
        if not re.fullmatch(r'^[a-zA-Z]+(?:-[a-zA-Z]+)*$', username):
            raise forms.ValidationError(
                "Логин должен содержать только латинские буквы и дефисы. "
                "Дефисы не могут быть в начале, в конце или идти подряд."
            )
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Размер файла не должен превышать 2 МБ.")
            ext = image.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'bmp']:
                raise forms.ValidationError("Разрешены только форматы: jpg, jpeg, png, bmp.")
        return image


class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['status', 'comment', 'design_image']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        design_image = cleaned_data.get("design_image")
        comment = cleaned_data.get("comment")

        if status == 'done' and not design_image:
            self.add_error('design_image', "Для статуса 'Выполнено' обязательно нужно прикрепить изображение дизайна.")
        if status == 'in_progress' and not comment:
            self.add_error('comment', "Для статуса 'Принято в работу' обязательно нужно указать комментарий.")
        return cleaned_data