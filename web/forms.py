from django import forms
from django.contrib.auth import get_user_model
from web.models import Recipe

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error("password", "Пароли не совпадают")
        return cleaned_data

    class Meta:
        model = User
        fields = ("email", "username", "password", "password2")


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RecipeFilterForm(forms.Form):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Поиск"}), required=False)
    difficulty = forms.ChoiceField(label="Сложность", choices=Recipe.DIFFICULTY_OPTIONS, required=False)
    cooking_time = forms.IntegerField(label="Время приготовления", required=False)


class ImportForm(forms.Form):
    file = forms.FileField()