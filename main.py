from flask import Flask, redirect, url_for, request, render_template, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_paginate import Pagination
from flask_principal import Principal, Permission, RoleNeed, identity_loaded, UserNeed, Identity, AnonymousIdentity, identity_changed
from flask_babel import Babel, _

app = Flask(__name__)

app.secret_key = "PeixeFrito123@"
app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
app.config['BABEL_SUPPORTED_LOCALES'] = ['pt', 'en']

login_manager = LoginManager(app)
login_manager.login_view = "login"
principals = Principal(app)
babel = Babel(app)

admin_permission = Permission(RoleNeed("admin"))
user_permission = Permission(RoleNeed("user"))

users = {
    "admin": {"password": "adminpass", "role": "admin"},
    "user": {"password": "userpass", "role": "user"}
}
products = [{"name": f"Produto {i}", "price": i * 10.0} for i in range(1, 51)]


class User(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.role = role


@login_manager.user_loader
def load_user(user_id):
    user_data = users.get(user_id)
    if user_data:
        return User(user_id, user_data["role"])
    return None


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    if current_user.is_authenticated:
        identity.provides.add(UserNeed(current_user.id))
        identity.provides.add(RoleNeed(current_user.role))


@babel.localeselector
def get_locale():
    return session.get('language', request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES']))


@app.route("/set_language/<language>")
def set_language(language):
    if language in app.config['BABEL_SUPPORTED_LOCALES']:
        session['language'] = language
        flash(_("Idioma alterado para {}.".format(language)), 'success')
    return redirect(request.referrer or url_for('index'))


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html", username=current_user.id, role=current_user.role)
    return render_template("index.html", username=None)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.get(username)
        if user and user["password"] == password:
            user_obj = User(username, user["role"])
            login_user(user_obj)
            return redirect(url_for("index"))
        flash(_("Credenciais inválidas. Por favor, tente novamente."), 'error')
        return render_template("login.html")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for("login"))


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
        return redirect(url_for("users_page"))
    return render_template("register.html")


@app.route("/users", methods=["GET"])
@login_required
def users_page():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = list(users.keys())[start:end]
    pagination = Pagination(page=page, total=len(users), per_page=per_page, record_name='users')
    return render_template('users.html', users=paginated_users, pagination=pagination)


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


@app.template_filter('currency')
def currency_filter(value):
    if value is None:
        return _('Preço não disponível')
    return f"R${value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


@app.route("/forbidden")
def forbidden():
    return render_template("403.html"), 403


if __name__ == "__main__":
    app.run(debug=True)
