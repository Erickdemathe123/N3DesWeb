Projeto N3DESWEB - Sistema Web em Flask com Login, Permissões e Traduções
Descrição
Este projeto consiste em uma aplicação web desenvolvida em Flask que utiliza autenticação, controle de permissões por papéis (admin e usuário), suporte a múltiplos idiomas (português e inglês) e paginação. Foi projetado para atender aos requisitos da disciplina de Desenvolvimento Web.

Pré-requisitos
Software necessário:

Python 3.10 ou superior
Pip (gerenciador de pacotes do Python)
Bibliotecas utilizadas:

Flask
Flask-Login
Flask-Babel
Flask-Principal
Flask-Paginate
Babel

Instale as dependências(pip install -r requirements.txt
)

Compile os arquivos de tradução
Certifique-se de que os arquivos .po (localizados em translations) estão corretos e execute o seguinte comando para compilar as traduções:(pybabel compile -d translations)


Inicie o servidor no terminal (flask run) ou de play no Pycharm
O servidor estará disponível em http://127.0.0.1:5000.

Funcionalidades
1. Idiomas
A aplicação suporta português e inglês.
O idioma pode ser alternado clicando nos links na parte inferior de cada página.
2. Login
Dois usuários pré-configurados para teste:
Admin: admin / adminpass
Usuário comum: user / userpass
3. Controle de Permissões
Admin:
Pode acessar todas as páginas, inclusive a de registro de novos usuários.
Usuário comum:
Não pode acessar páginas administrativas (recebe um erro 403).
4. Registro de Usuários
Apenas o admin pode registrar novos usuários.
5. Paginação
A aplicação inclui paginação na exibição de usuários e produtos.
Testes Funcionais

Alteração de idioma:
Na página inicial ou em qualquer outra página, clique nos links Português ou English e confira se o idioma muda corretamente.

Login funcional:
Acesse /login e teste as credenciais fornecidas:
Admin: admin / adminpass
Usuário comum: user / userpass

Registro de novos usuários:
Faça login como admin.
Acesse a página de registro, insira os dados e registre um novo usuário.
Teste o login com o novo usuário.

Controle de permissões:
Como admin, tente acessar todas as páginas.
Como usuário comum, tente acessar páginas restritas, como /register e /users, e confira se o acesso é negado.

Paginação:
Acesse a página /products e use os botões de paginação para navegar entre as páginas.
