🚗 Gestão de Aluguel de Veículos
📌 Sobre o Projeto
Este projeto é uma aplicação web para gestão de aluguel de veículos, permitindo administrar a frota, aluguéis, inspeções e revisões de forma organizada.

🛠 Tecnologias Utilizadas
Django (Backend)

Bootstrap 5 (Frontend)

PostgreSQL (Banco de Dados)

HTML, CSS, JavaScript (Interface)

🔧 Instalação
Clone o repositório:

bash
git clone https://github.com/ClaudioFritzen/Luxury-Wheels
Acesse a pasta do projeto:

bash
cd SeuProjeto
Crie e ative um ambiente virtual:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
Instale as dependências:

bash
pip install -r requirements.txt
Faça as migrações do banco de dados:

bash
python manage.py migrate
Crie um superusuário:

bash
python manage.py createsuperuser
Inicie o servidor:

bash
python manage.py runserver
🚀 Funcionalidades
✅ Cadastro e edição de veículos ✅ Gerenciamento de aluguéis ativos ✅ Controle de inspeções e revisões ✅ Relatórios de veículos mais alugados

📄 Como Usar
Acesse http://localhost:8000/admin para gerenciar usuários.

Utilize a interface principal para acessar veículos e aluguéis.

Os relatórios ajudam a visualizar tendências de aluguel e revisões.
