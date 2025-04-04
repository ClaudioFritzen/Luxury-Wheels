from django.test import TestCase, Client
from django.urls import reverse
from .test_models import Usuario

class UsuarioViewTestCase(TestCase):
    def setUp(self):
        """Configuração inicial: cria um usuario de teste"""
        self.objeto = Usuario.objects.create(
            primeiro_nome="João",
            ultimo_novo="Silva",
            email="joao@email.com",
            user="joaosilva",
            password="SenhaForte123!"
        )
    
    def test_listar_usuarios(self):
        # Testa se a view retorna a lista de usuários corretamente
        response = self.client.get(reverse("usuario_list")) ## Certifique-se que essa url ja esta criada
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "joaosilva")



    def test_criacao_usuario(self):
        """Testa se o usuario foi criado corretamente """
        self.assertEqual(self.usuario.primeiro_nome, "João")
        self.assertEqual(self.usuario.ultimo_nome, "Silva")
        self.assertEqual(self.usuario.email, "joao@email.com")
        self.assertEqual(self.usuario.username, "joaosilva")
        self.assertEqual(self.usuario.password.startwith,("pbkdf2_"))()

