from flask import Flask, redirect, url_for, request, render_template, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_paginate import Pagination
from flask_principal import Principal, Permission, RoleNeed, identity_loaded, UserNeed, Identity, AnonymousIdentity, identity_changed
from flask_babel import Babel, _

app = Flask(__name__)

# Configurações principais
app.secret_key = "PeixeFrito123@"
app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
app.config['BABEL_SUPPORTED_LOCALES'] = ['pt', 'en']

# Inicializações
login_manager = LoginManager(app)
login_manager.login_view = "login"
principals = Principal(app)
babel = Babel(app)

# Definição de permissões
admin_permission = Permission(RoleNeed("admin"))
user_permission = Permission(RoleNeed("user"))

# Usuários e produtos (simulação de banco de dados)
users = {
    "admin": {"password": "adminpass", "role": "admin"},
    "user": {"password": "userpass", "role": "user"}
}
products = [{"name": f"Produto {i}", "price": i * 10.0} for i in range(1, 51)]

# Modelo de usuário
class User(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.role = role

# Função para carregar usuário
@login_manager.user_loader
def load_user(user_id):
    user_data = users.get(user_id)
    if user_data:
        return User(user_id, user_data["role"])
    return None

# Callback para carregar identidade de usuários autenticados
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    if current_user.is_authenticated:
        identity.provides.add(UserNeed(current_user.id))
        identity.provides.add(RoleNeed(current_user.role))

# Seleção de idioma
@babel.localeselector
def get_locale():
    return session.get('language', request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES']))

# Rota para alterar idioma
@app.route("/set_language/<language>")
def set_language(language):
    if language in app.config['BABEL_SUPPORTED_LOCALES']:
        session['language'] = language
        flash(_("Idioma alterado para {}.".format(language)), 'success')
    return redirect(request.referrer or url_for('index'))

# Página inicial
@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html", username=current_user.id, role=current_user.role)
    return render_template("index.html", username=None)

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.get(username)
        if user and user["password"] == password:
            user_obj = User(username, user["role"])
            login_user(user_obj)
            identity_changed.send(app, identity=Identity(user_obj.id))
            return redirect(url_for("index"))
        flash(_("Credenciais inválidas. Por favor, tente novamente."), 'error')
    return render_template("login.html")

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    identity_changed.send(app, identity=AnonymousIdentity())
    flash(_("Você saiu com sucesso."), 'success')
    return redirect(url_for("login"))

# Registro (somente admin)
@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if not admin_permission.can():
        return redirect(url_for('forbidden'))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        if username in users:
            flash(_("Este nome de usuário já está em uso. Tente outro."), 'error')
            return render_template("register.html")

        users[username] = {"password": password, "role": role}
        flash(_("Usuário registrado com sucesso!"), 'success')
        return redirect(url_for("users_page"))
    return render_template("register.html")

# Página de usuários (somente admin)
@app.route("/users", methods=["GET"])
@login_required
def users_page():
    if not admin_permission.can():
        return redirect(url_for('forbidden'))
    page = request.args.get('page', 1, type=int)
    per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = list(users.keys())[start:end]
    pagination = Pagination(page=page, total=len(users), per_page=per_page, record_name='users')
    return render_template('users.html', users=paginated_users, pagination=pagination)

# Página de produtos (qualquer usuário autenticado)
@app.route("/products", methods=["GET"])
@login_required
def products_page():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    paginated_products = products[start:end]
    pagination = Pagination(page=page, total=len(products), per_page=per_page, record_name='products')
    return render_template('products.html', products=paginated_products, pagination=pagination)

# Filtro de preço
@app.template_filter('currency')
def currency_filter(value):
    if value is None:
        return _('Preço não disponível')
    return f"R${value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Página de erro 403
@app.route("/forbidden")
def forbidden():
    return render_template("403.html", message=_("Acesso negado: você não tem permissão para acessar esta página.")), 403

# Executar o aplicativo
if __name__ == "__main__":
    app.run(debug=True)
s