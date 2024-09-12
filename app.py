from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from cryptography.fernet import Fernet
import os

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///password_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Replace with a strong secret key
app.config['SECRET_KEY'] = Fernet.generate_key().decode()  # Generate and store securely

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
fernet = Fernet(app.config['SECRET_KEY'])

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Password model
class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    website = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token})

@app.route('/add_password', methods=['POST'])
@jwt_required()
def add_password():
    data = request.get_json()
    current_user = get_jwt_identity()
    encrypted_password = fernet.encrypt(data['password'].encode()).decode()
    new_password = Password(user_id=current_user, website=data['website'],
                            username=data['username'], password=encrypted_password)
    db.session.add(new_password)
    db.session.commit()
    return jsonify({'message': 'Password saved successfully'})

@app.route('/get_passwords', methods=['GET'])
@jwt_required()
def get_passwords():
    current_user = get_jwt_identity()
    passwords = Password.query.filter_by(user_id=current_user).all()
    result = []
    for password in passwords:
        result.append({
            'website': password.website,
            'username': password.username,
            'password': fernet.decrypt(password.password.encode()).decode()
        })
    return jsonify(result)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
