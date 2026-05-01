from flask import Blueprint, request, jsonify
from models import Admin
from extensions import db, bcrypt
from flask_login import login_user, logout_user
from itsdangerous import URLSafeTimedSerializer

auth_bp = Blueprint('auth', __name__)
serializer = URLSafeTimedSerializer("SECRET_KEY")


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json

    if Admin.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Account already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = Admin(
        full_name=data['full_name'],
        email=data['email'],
        password=hashed_pw
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Signup successful"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = Admin.query.filter_by(email=data['email']).first()

    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    login_user(user, remember=data.get("remember", False))
    return jsonify({"message": "Login successful"})


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    user = Admin.query.filter_by(email=data['email']).first()

    if user:
        token = serializer.dumps(user.email)
        print(f"Reset link: http://localhost:5000/reset/{token}")

    return jsonify({"message": "If email exists, reset link sent"})


@auth_bp.route('/reset/<token>', methods=['POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, max_age=3600)
    except:
        return jsonify({"error": "Token expired"}), 400

    user = Admin.query.filter_by(email=email).first()
    data = request.json

    user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    db.session.commit()

    return jsonify({"message": "Password updated"})