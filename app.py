from flask import Flask, redirect,  url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user

# CONFIGURATIONS
app = Flask(__name__,  static_url_path='/static')
app.secret_key = "@ui561zX"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://flask_with_auth_user:qJ1JI3SIIyqrS0CDSscK4Z3dAEbjot7h@dpg-cptlki1u0jms73eb67dg-a.singapore-postgres.render.com/flask_with_auth"
# LOCAL DATABASE: "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "$d771yKt"
db = SQLAlchemy()

# LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)

# DATABASE MODEL
class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)

# INITIALIZING THE DATABASE
db.init_app(app)

with app.app_context():
	db.create_all()
     
# LOADING USER
@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)

# ROUTES
@app.route("/")
def home():
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        user = session["user"]
        name = str(user).title()
        return render_template("dashboard.html", user=name)
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form.get("username")).first()
        if user is None:
             return redirect(url_for("login"))
        else:
            if user.password == request.form.get("password"):
                name = request.form.get("username")
                session["user"] = name
                login_user(user)
                return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = Users(username=request.form.get("username"), password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run()
