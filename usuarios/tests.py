from django.test import TestCase
from .models import Usuario # Importa o modelo Usuario
from django.contrib.auth.hashers import check_password


# Create your tests here.
class UsuarioTestCase(TestCase):
    # função para criar um usuário
    def test_create_user(self):
        ## Passando os dados do usuário
        user = Usuario.objects.create(
            primeiro_nome='João',
            ultimo_nome='Silva',
            email='joao@gmail.com',
            username='joaosilva',
            password='12345678'
        )

        # Verifica se o usuário foi criado corretamente
        self.assertEqual(user.primeiro_nome, 'João')
        self.assertEqual(user.ultimo_nome, 'Silva')
        self.assertEqual(user.email, 'joao@gmail.com')


## Teste para verificar se a senha do usuário foi criptografada
from django.test import TestCase
from django.contrib.auth.hashers import check_password
from .models import Usuario

class UsuarioPasswordTestCase(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create(
            primeiro_nome='Maria',
            ultimo_nome='Santos',
            email="maria@email.com",
            username='mariasantos',
            password='minhasenha1234'  # O nome correto do campo é password
        )

    def test_password_encryption(self):
        """Verifica se a senha foi criptografada corretamente."""
        self.user.refresh_from_db()  # Garante que estamos pegando o valor atualizado do banco
        self.assertNotEqual(self.user.password, 'minhasenha1234')  # Agora acessando corretamente `password`
        self.assertTrue(check_password('minhasenha1234', self.user.password))  # Comparação correta

