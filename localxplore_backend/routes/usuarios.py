from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Usuario
import re

usuarios_bp = Blueprint('usuarios', __name__)

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@usuarios_bp.route('', methods=['GET'])
@jwt_required()
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios]), 200

@usuarios_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify(usuario.to_dict()), 200

@usuarios_bp.route('', methods=['POST'])
@jwt_required()
def create_usuario():
    data = request.get_json()
    
    # Validaciones
    required = ['nombre', 'apellido', 'email', 'password', 'rol']
    for field in required:
        if not data.get(field):
            return jsonify({"msg": f"El campo {field} es obligatorio"}), 400

    if len(data['password']) < 8:
        return jsonify({"msg": "La contraseña debe tener al menos 8 caracteres"}), 400
    
    if not validar_email(data['email']):
        return jsonify({"msg": "Formato de email inválido"}), 400

    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "El email ya está registrado"}), 409

    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        apellido=data['apellido'],
        email=data['email'],
        rol=data['rol'],
        telefono=data.get('telefono'),
        ciudad=data.get('ciudad'),
        estado=data.get('estado', True)
    )
    nuevo_usuario.set_password(data['password'])
    
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    return jsonify(nuevo_usuario.to_dict()), 201

@usuarios_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    data = request.get_json()

    if 'email' in data and data['email'] != usuario.email:
        if not validar_email(data['email']):
            return jsonify({"msg": "Formato de email inválido"}), 400
        if Usuario.query.filter_by(email=data['email']).first():
            return jsonify({"msg": "El email ya está registrado"}), 409
        usuario.email = data['email']

    if 'password' in data and data['password']:
        if len(data['password']) < 8:
            return jsonify({"msg": "La contraseña debe tener al menos 8 caracteres"}), 400
        usuario.set_password(data['password'])

    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.apellido = data.get('apellido', usuario.apellido)
    usuario.rol = data.get('rol', usuario.rol)
    usuario.telefono = data.get('telefono', usuario.telefono)
    usuario.ciudad = data.get('ciudad', usuario.ciudad)
    usuario.estado = data.get('estado', usuario.estado)

    db.session.commit()
    return jsonify(usuario.to_dict()), 200

@usuarios_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_usuario(id):
    current_user_id = get_jwt_identity()
    if str(id) == str(current_user_id):
        return jsonify({"msg": "No puedes eliminarte a ti mismo"}), 403

    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    
    return jsonify({"msg": "Usuario eliminado correctamente"}), 200
