from django.test import TestCase
from django.core.exceptions import ValidationError
from usuarios.models import Usuario

# validação do email unico
from django.db.utils import IntegrityError


class UsuarioTestCase(TestCase):

    def test_create_user(self):
        """Testa se um usuário válido é criado com sucesso"""
        user = Usuario(
            primeiro_nome='João',
            ultimo_nome='Silva',
            email='joao@gmail.com',
            username='joaosilva',
            password='Senha123!'
        )
        user.full_clean()  # Valida os campos antes de salvar
        user.save()  # Salva no banco de dados

        # Verifica se o usuário foi salvo
        self.assertIsNotNone(user.id)

        # Verifica se os dados estão corretos
        self.assertEqual(user.primeiro_nome, 'João')
        self.assertEqual(user.ultimo_nome, 'Silva')
        self.assertEqual(user.email, 'joao@gmail.com')

    def test_senha_apenas_numeros(self):
        """Testa se uma senha composta apenas por números é rejeitada"""
        with self.assertRaises(ValidationError) as e:
            user = Usuario(
                primeiro_nome='João',
                ultimo_nome='Silva',
                email='teste@email.com',
                username='joaosilva',
                password='12345'
            )
            user.full_clean()  # Dispara os erros de validação

        erro_msgs = e.exception.messages
        print("Mensagens de erro capturadas:", erro_msgs)

        if len(user.password) < 8:
            self.assertIn(
                'A senha deve ter pelo menos 8 caracteres.', erro_msgs)
        # self.assertIn('A senha deve ter pelo menos 8 caracteres.', erro_msgs)
        self.assertIn(
            'A senha deve conter pelo menos uma letra maiúscula.', erro_msgs)
        self.assertIn(
            'A senha deve conter pelo menos um caractere especial.', erro_msgs)

    # TODO teste de senha curta

    def test_senha_curta(self):
        with self.assertRaises(ValidationError) as e:
            user = Usuario(
                primeiro_nome="Teste",
                ultimo_nome="Usuario",
                email="teste@email.com",
                username="testeuser",
                password="Ab1!"
            )
            user.full_clean()

        # print("Erro capturado:", str(e.exception))
        self.assertIn('A senha deve ter pelo menos 8 caracteres.',
                      str(e.exception))

    # TODO teste de senha sem letras maiusculas

    def test_senha_sem_letras_maiusculas(self):
        with self.assertRaises(ValidationError) as e:
            user = Usuario(
                primeiro_nome="Teste",
                ultimo_nome="Usuario",
                email="teste@email.com",
                username="testeuser",
                password="senha123!"
            )
            user.full_clean()

        print("Erro capturado:", str(e.exception))
        self.assertIn(
            'A senha deve conter pelo menos uma letra maiúscula.', str(e.exception))

    # TODO teste de senha sem caracteres especiais
    def test_senha_sem_caracter_especial(self):
        with self.assertRaises(ValidationError) as e:
            user = Usuario(
                primeiro_nome="Teste",
                ultimo_nome="Usuario",
                email="teste@email.com",
                username="testeuser",
                password="Senha123"
            )
            user.full_clean()
        print("Erro capturado:", str(e.exception))
        self.assertIn(
            'A senha deve conter pelo menos um caractere especial.', str(e.exception))

    # TODO teste de senha sem numeros
    def test_senha_sem_numeros(self):
        with self.assertRaises(ValidationError) as e:
            user = Usuario(
                primeiro_nome="Teste",
                ultimo_nome="Usuario",
                email="teste@email.com",
                username="testeuser",
                password="Abcdefg!"
            )
            user.full_clean()
        print("Erro capturado:", str(e.exception))
        self.assertIn('A senha deve conter pelo menos um número.',
                      str(e.exception))

    # TODO teste de senha com todos os requisitos
    def test_senha_com_todos_requisitos(self):
        """Testa se uma senha válida passa na validação"""
        try:
            user = Usuario(
                primeiro_nome="Teste",
                ultimo_nome="Usuario",
                email="teste@email.com",
                username="testeuser",
                password="Abcd1234!!"  # Senha válida
            )
            user.full_clean()  # Deve passar sem erro
        except ValidationError as e:
            # Se cair aqui, falha o teste
            self.fail(f"Erro inesperado ao validar senha válida: {e}")

    # TODO teste de senha com espaços no início e no final

    def test_senha_com_espacos_inicio_e_final(self):
        """Testa se espaços no início e no final da senha não afetam a validação"""
        user = Usuario(
            primeiro_nome="Teste",
            ultimo_nome="Usuario",
            email="teste@email.com",
            username="testeuser",
            password="  Abcd1234!  "  # Senha válida, mas com espaços extras
        )

        try:
            user.full_clean()  # Deve passar sem erro
        except ValidationError as e:
            self.fail(f"Erro inesperado: {e}")  # Falha o teste se houver erro

    # TODO teste com senhas no inicio e no final removidas
    def test_senha_com_espacos_removidos(self):
        with self.assertRaises(ValidationError) as e:
            user = Usuario(
                primeiro_nome="Teste",
                ultimo_nome="Usuario",
                email="teste@email.com",
                username="testeuser",
                password="  Ab1234!  "  # Senha invalida, revomendo os espaços fica menor que 8 caracteres
            )

            user.full_clean()  # Deve passar sem erro

        print("Erro capturado:", str(e.exception))
        self.assertIn('A senha deve ter pelo menos 8 caracteres.',
                      str(e.exception))

    # TODO teste de senha com espaços no meio

    def test_senha_com_espacos_no_meio(self):
        """Testa se espaços no meio da senha são considerados inválidos"""
        with self.assertRaises(ValidationError) as e:
            user = Usuario(
                primeiro_nome="Teste",
                ultimo_nome="Usuario",
                email="teste@email.com",
                username="testeuser",
                password="Abc 1234!"  # Senha inválida com espaço no meio
            )
            user.full_clean()

        self.assertIn(
            "A senha não pode conter espaços em branco no meio.", str(e.exception))

    # TODO teste de email duplicado e do tipo email
    def test_criar_um_usuario_com_email_valido(self):
        # Testa se um usuário com email válido é criado com sucesso
        user = Usuario(
            primeiro_nome="Teste",
            ultimo_nome="Usuario",
            email="teste@email.com",
            username="testeuser",
            password="Abcd1234!"
        )

        self.assertIsNone(user.id)  # Ainda não foi salvo
        self.assertEqual(user.email, "teste@email.com")

    def test_email_deve_ser_unico(self):
        """Testa se um erro é lançado ao tentar criar um usuário com email duplicado"""

        # Criando o primeiro usuário (mas sem chamar `full_clean()` diretamente)
        Usuario.objects.create(
            primeiro_nome="Teste",
            ultimo_nome="Usuario",
            email="teste@gmail.com",
            username="testeuser",
            password="Abcd1234!"
        )

        # Agora tentamos criar o segundo usuário com o mesmo e-mail
        with self.assertRaises(ValidationError) as e:
            user_duplicado = Usuario(
                primeiro_nome="TesteFulano",
                ultimo_nome="emailigual",
                email="teste@gmail.com",  # Email duplicado
                username="testeuser112",
                password="Abcd1234!"
            )
            user_duplicado.full_clean()  # Aqui o erro deve ser chamado

        # Verifica se a chave 'email' está nos erros
        self.assertIn('email', e.exception.message_dict)

        # verifica se a mensagem de erro é a esperada
        mensagem_erro = e.exception.message_dict['email'][0]
        self.assertIn(mensagem_erro, "Usuario with this Email already exists.")

        print("Erro capturado:", str(e.exception))
        print("Mensagem de erro:", mensagem_erro)

    def test_email_invalido(self):
        with self.assertRaises(ValidationError) as e:
            user = Usuario(
                primeiro_nome="Teste",
                ultimo_nome="Usuario",
                email="emailinvalido.com",  # Email inválido
                username="testeuser",
                password="Abcd1234!"
            )
            user.full_clean()
        mensagem_erro = e.exception.message_dict

        self.assertIn("email", mensagem_erro)  # Verifica o erro
        print(f"Erro Capturado: {mensagem_erro}")
        # verifica se a mensagem "Enter a valid email adress." está na lista de erros para o email
        self.assertIn("Enter a valid email address.", mensagem_erro['email'])

    def test_email_vazio(self):
        # Testa se um erro é lançado ao tentar criar um usuário com email vazio
        with self.assertRaises(ValidationError) as e:
            user = Usuario(
                primeiro_nome="Teste",
                ultimo_nome="Usuario",
                email="",
                username="testeuser",
                password="Abcd1234!"
            )

            user.full_clean()

        mensagem_erro = e.exception.message_dict
        print("Erro capturado", mensagem_erro)

        # verificando se o erro esperado esta presente
        self.assertIn("email", mensagem_erro,
                      "O campo 'email' deveria estar na lista de erros.")
        self.assertIn("This field cannot be blank.",
                      mensagem_erro['email'], "A mensagem de erro esperada não foi encontrada")

    def test_username_deve_ser_unico(self):
        Usuario.objects.create(
            primeiro_nome="Teste",
            ultimo_nome="Usuario",
            email='teste@email.com',
            username="testeuser",
            password='Abcd1234!'
        )

        # Tenta criar um usuario com o mesmo username
        with self.assertRaises(ValidationError) as e:
            username_duplicado = Usuario(
                primeiro_nome="novo",
                ultimo_nome="user",
                email='bloco@email.com',
                username="testeuser",
                password='Abcd1234!'
            )

            username_duplicado.full_clean()

        mensagem_erro = e.exception.message_dict
        print(f"Erro capturado: {mensagem_erro}")
        self.assertIn('username', mensagem_erro)
        self.assertIn('Usuario with this Username already exists.', mensagem_erro['username'])

    def test_username_nao_deve_ser_vazio(self):
        with self.assertRaises(ValidationError) as e:
            user = Usuario(
                primeiro_nome="Teste",
                ultimo_nome="Usuario",
                email="teste@gmail.com",
                username="",  # Username vazio
                password="Abcd1234!"
            )
            user.full_clean()  # ❗️ Isso deve estar dentro do `with`

        mensagem_erro = e.exception.message_dict
        print(f"Erro Capturado: {mensagem_erro}")

        self.assertIn("username", mensagem_erro)
        self.assertIn("This field cannot be blank.", mensagem_erro["username"])
