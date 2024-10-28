"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Colaborador, Tarea, Oportunidad
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User
from datetime import datetime


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

    

     # Si el rol es 'colaborador', también crear un colaborador
    if nuevo_usuario.rol == 'colaborador':
        nuevo_colaborador = Colaborador(
            nombre=nuevo_usuario.nombre,  # Puedes almacenar más información si es necesario
            email=nuevo_usuario.email,
            user_id=nuevo_usuario.id  # Relacionar al colaborador con el usuario
        )
        
        db.session.add(nuevo_colaborador)
        db.session.commit()  # Guarda el nuevo colaborador en la base de datos

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

    return jsonify({"usuario_con_acceso": user_id, "msg": "Acceso autorizado"}), 200


# Endpoint para obtener todos los colaboradores
@api.route('/colaboradores', methods=['GET'])
@jwt_required()
def get_colaboradores():
    try:
        colaboradores = Colaborador.query.all()
        serialized_colaboradores = [colaborador.serialize() for colaborador in colaboradores]
        return jsonify(serialized_colaboradores), 200
    
    except Exception as e:
        return jsonify({'msg': 'Error al recuperar colaboradores', 'error': str(e)}), 500
    

# Endpoint para obtener todos los usuarios
@api.route('/usuarios', methods=['GET'])
@jwt_required()
def get_usuarios():
    try:
        usuarios = User.query.all()
        serialized_usuarios = [usuario.serialize() for usuario in usuarios]
        return jsonify(serialized_usuarios), 200
    
    except Exception as e:
        return jsonify({'msg': 'Error al recuperar usuarios', 'error': str(e)}), 500
    

# Endpoint para agregar una tarea a una oportunidad específica
@api.route('/oportunidades/<int:oportunidad_id>/tareas', methods=['POST'])
@jwt_required()
def agregar_tarea(oportunidad_id):
    try:
        # Obtener la oportunidad según el ID pasado en la URL
        oportunidad = Oportunidad.query.get(oportunidad_id)
        
        # Si la oportunidad no existe, retornar un error
        if not oportunidad:
            return jsonify({'msg': 'Oportunidad no encontrada'}), 404
        
        # Obtener los datos de la tarea desde el cuerpo de la solicitud
        titulo = request.json.get('titulo')
        descripcion = request.json.get('descripcion')
        estado = request.json.get('estado', 'pendiente')
        fecha_vencimiento = request.json.get('fecha_vencimiento')
        colaborador_id = request.json.get('colaborador_id')

        # Crear la nueva tarea
        nueva_tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            estado=estado,
            fecha_vencimiento=fecha_vencimiento,
            oportunidad_id=oportunidad_id,
            colaborador_id=colaborador_id
        )

        # Agregar la nueva tarea a la sesión y guardar los cambios en la base de datos
        db.session.add(nueva_tarea)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tarea creada exitosamente',
            'tarea': nueva_tarea.serialize()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Error al crear la tarea', 'error': str(e)}), 500
    


# Endpoint para asignar una tarea a un colaborador
@api.route('/oportunidades/<int:oportunidad_id>/tareas/<int:tarea_id>/asignar', methods=['POST'])
@jwt_required()
def asignar_tarea(oportunidad_id, tarea_id):
    try:
        # Buscar la tarea por su ID
        tarea = Tarea.query.filter_by(id=tarea_id, oportunidad_id=oportunidad_id).first()
        
        # Verificar si la tarea existe y pertenece a la oportunidad indicada
        if not tarea:
            return jsonify({'msg': 'Tarea no encontrada o no pertenece a la oportunidad especificada'}), 404
        
        # Obtener el ID del colaborador desde el JSON de la solicitud
        colaborador_id = request.json.get('colaborador_id', None)
        
        # Validar que se haya enviado el colaborador_id
        if not colaborador_id:
            return jsonify({'msg': 'colaborador_id es requerido'}), 400
        
        # Asignar el colaborador a la tarea
        tarea.colaborador_id = colaborador_id
        
        # Guardar los cambios en la base de datos
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tarea asignada exitosamente al colaborador',
            'tarea': tarea.serialize()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Error al asignar la tarea', 'error': str(e)}), 500




# Endpoint para crear una nueva Oportunidad
@api.route('/oportunidades', methods=['POST'])
@jwt_required()
def crear_oportunidad():
    try:
        # Obtener los datos de la solicitud JSON
        titulo = request.json.get('titulo', None)
        descripcion = request.json.get('descripcion', None)
        estado = request.json.get('estado', 'disponible')  # Estado por defecto es 'disponible'
        colaborador_id = request.json.get('colaborador_id', None)
        
        # Validar los datos requeridos
        if not descripcion:
            return jsonify({"msg": "La descripción es requerida"}), 400

        # Crear la nueva oportunidad
        nueva_oportunidad = Oportunidad(
            titulo=titulo,
            descripcion=descripcion,
            estado=estado,
            colaborador_id=colaborador_id
        )

        # Agregar la oportunidad a la sesión y guardar en la base de datos
        db.session.add(nueva_oportunidad)
        db.session.commit()

        # Responder con la oportunidad creada
        return jsonify({
            "success": True,
            "message": "Oportunidad creada exitosamente",
            "oportunidad": nueva_oportunidad.serialize()
        }), 201

    except Exception as e:
        # Manejar errores y devolver mensaje de error
        return jsonify({"msg": "Error al crear la oportunidad", "error": str(e)}), 500
    
    # Endpoint para obtener todas las oportunidades
@api.route('/oportunidades', methods=['GET'])
@jwt_required()
def get_oportunidades():
    try:
        oportunidades = Oportunidad.query.all()
        serialized_oportunidades = [oportunidad.serialize() for oportunidad in oportunidades]
        return jsonify(serialized_oportunidades), 200
    
    except Exception as e:
        return jsonify({'msg': 'Error al recuperar oportunidades', 'error': str(e)}), 500
    

    # Endpoint para actualizar una oportunidad (PUT)
@api.route('/oportunidades/<int:oportunidad_id>', methods=['PUT'])
@jwt_required()
def actualizar_oportunidad(oportunidad_id):
    try:
        # Buscar la oportunidad por su ID
        oportunidad = Oportunidad.query.get(oportunidad_id)
        
        # Si la oportunidad no existe, retornar un error
        if not oportunidad:
            return jsonify({'msg': 'Oportunidad no encontrada'}), 404
        
        # Obtener los datos del cuerpo de la solicitud JSON
        titulo = request.json.get('titulo', oportunidad.titulo)  # Mantener el valor actual si no se envía
        descripcion = request.json.get('descripcion', oportunidad.descripcion)
        estado = request.json.get('estado', oportunidad.estado)
        colaborador_id = request.json.get('colaborador_id', oportunidad.colaborador_id)
        
        # Actualizar los valores de la oportunidad
        oportunidad.titulo = titulo
        oportunidad.descripcion = descripcion
        oportunidad.estado = estado
        oportunidad.colaborador_id = colaborador_id
        
        # Guardar los cambios en la base de datos
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Oportunidad actualizada exitosamente",
            "oportunidad": oportunidad.serialize()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Error al actualizar la oportunidad', 'error': str(e)}), 500


# Endpoint para eliminar una oportunidad (DELETE)
@api.route('/oportunidades/<int:oportunidad_id>', methods=['DELETE'])
@jwt_required()
def eliminar_oportunidad(oportunidad_id):
    try:
        # Buscar la oportunidad por su ID
        oportunidad = Oportunidad.query.get(oportunidad_id)
        
        # Si la oportunidad no existe, retornar un error
        if not oportunidad:
            return jsonify({'msg': 'Oportunidad no encontrada'}), 404
        
        # Eliminar la oportunidad de la base de datos
        db.session.delete(oportunidad)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Oportunidad eliminada exitosamente"
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Error al eliminar la oportunidad', 'error': str(e)}), 500

@api.route('/oportunidades/<int:oportunidad_id>/apuntarse', methods=['POST'])
@jwt_required()
def apuntarse_oportunidad(oportunidad_id):
    try:
        # Obtener el colaborador autenticado a partir del token JWT
        user_id = get_jwt_identity()  # Asegúrate de que get_jwt_identity devuelva el ID del colaborador

        # Buscar la oportunidad por su ID
        oportunidad = Oportunidad.query.get(oportunidad_id)
        
        # Verificar que la oportunidad existe
        if not oportunidad:
            return jsonify({'msg': 'Oportunidad no encontrada'}), 404

        # Verificar si ya tiene un colaborador asignado
        if oportunidad.colaborador_id is not None:
            return jsonify({'msg': 'Esta oportunidad ya tiene un colaborador asignado'}), 400

        # Asignar el colaborador a la oportunidad
        oportunidad.colaborador_id = user_id

        # Guardar los cambios en la base de datos
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Te has apuntado a la oportunidad exitosamente",
            "oportunidad": oportunidad.serialize()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Error al apuntarse a la oportunidad', 'error': str(e)}), 500
