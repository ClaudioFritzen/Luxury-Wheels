from django import forms
from django.core.exceptions import ValidationError

from .models import Usuario
from django.contrib.auth.hashers import make_password
from usuarios.validators import validar_senha  # ✅ Importa a função de validação

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = Usuario
        fields = ['primeiro_nome', 'ultimo_nome', 'email', 'username', 'password']

    def clean_password(self):
        """Valida a senha antes de salvar"""
        password = self.cleaned_data.get("password")
        validar_senha(password)  # ✅ Chama a função de validação
        return password

    def clean(self):
        """Verifica se as senhas correspondem"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("As senhas não coincidem.")

        return cleaned_data

    def save(self, commit=True):
        """Criptografa a senha antes de salvar"""
        usuario = super().save(commit=False)
        usuario.password = make_password(self.cleaned_data["password"])  # 🔒 Criptografa a senha

        if commit:
            usuario.save()
        return usuario
