from django.test import TestCase
from django.core.exceptions import ValidationError
from usuarios.models import Usuario

class UsuarioPasswordValidationTestCase(TestCase):

    def test_senha_invalida_menos_8_caracteres(self):
        with self.assertRaises(ValidationError) as e:
            Usuario(password="Aa1!").full_clean()
        self.assertIn("A senha deve ter pelo menos 8 caracteres.", str(e.exception))

    def test_senha_sem_maiuscula(self):
        with self.assertRaises(ValidationError) as e:
            Usuario(password="abcd1234!").full_clean()
        self.assertIn("A senha deve conter pelo menos uma letra maiúscula.", str(e.exception))

    def test_senha_sem_numero(self):
        with self.assertRaises(ValidationError) as e:
            Usuario(password="Abcdefg!").full_clean()
        self.assertIn("A senha deve conter pelo menos um número.", str(e.exception))

    def test_senha_sem_caractere_especial(self):
        with self.assertRaises(ValidationError) as e:
            Usuario(password="Abcd1234").full_clean()
        self.assertIn("A senha deve conter pelo menos um caractere especial", str(e.exception))

    def test_senha_valida(self):
        try:
            Usuario(password="Senha123!").full_clean()
        except ValidationError:
            self.fail("Uma senha válida foi rejeitada incorretamente.")
