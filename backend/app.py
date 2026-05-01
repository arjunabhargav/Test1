from flask import Flask
from flask_cors import CORS
from extensions import db, login_manager, bcrypt
from routes.auth import auth_bp
from routes.opportunity import opp_bp

app = Flask(__name__)

CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5500"])

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)

login_manager.login_view = "auth.login"


from models import Admin

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(opp_bp, url_prefix='/opportunity')

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
