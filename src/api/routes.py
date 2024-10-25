"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)



#RUTA PARA REGISTRO DE USUARIO
@api.route('/registro', methods=['POST'])
def registro():
    nombre = request.json.get('nombre', None)
    email = request.json.get('email', None)
    contraseña = request.json.get('contraseña', None)
    rol = request.json.get('rol', None)

    if not email or not nombre or not contraseña or not rol:
        return jsonify({'msg': 'Email, nombre, contraseña y rol son requeridos'}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'msg': 'El email ya está registrado'}), 409  # Código 409: conflicto (email duplicado)

    # Hasheo la contraseña antes de almacenarla
    hashed_password = generate_password_hash(contraseña)
    
    # Agrego el nuevo usuario a la base de datos
    nuevo_usuario = User(
    nombre=nombre,  # Asignamos el nombre
    email=email,
    contraseña=hashed_password,
    rol=rol  # Asignamos el rol
)

    # Agrego el nuevo usuario a la base de datos
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'msg': 'Usuario registrado con éxito', 'user_id': nuevo_usuario.id}), 201


# Login de usuario y devuelve un token
@api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    contraseña = request.json.get('contraseña', None)
    
    # Verifico que se ingresen datos
    if not email or not contraseña:
        return jsonify({'msg': 'Email y contraseña son requeridos'}), 400
    
    # Busco al usuario en la base de datos por el email
    user = User.query.filter_by(email=email).first()
    
    # Verifico si el usuario no fue encontrado o la contraseña no coincide
    if not user or not check_password_hash(user.contraseña, contraseña):
        return jsonify({'msg': 'Email o contraseña incorrectos'}), 401
    
    # Si el usuario es ok, genero el token JWT
    token_creado = create_access_token(identity=user.id)
    
    # Devuelvo el token y el ID del usuario
    return jsonify({'token': token_creado, 'user_id': user.id}), 200

# Ruta privada
@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    user_id = get_jwt_identity()

    # simepre que quiera devolver un json debo utilizar un diccionario en en return
    return jsonify({"usuario_con_acceso": user_id, "msg": "Acceso autorizado"}), 200