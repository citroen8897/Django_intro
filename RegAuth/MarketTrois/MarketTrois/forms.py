from django import forms


class AuthForm(forms.Form):
    login = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        min_length=6)


class RegForm(forms.Form):
    login = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        min_length=6)
    password_rep = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}),
        min_length=6)
    nom = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    prenom = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Фамилия'}))
    telephone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Телефон'}))


class CategoryForm(forms.Form):
    nom = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название категории'}))
