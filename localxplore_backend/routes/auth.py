from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email y contraseña son requeridos"}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and usuario.check_password(password):
        if not usuario.estado:
            return jsonify({"msg": "Usuario inactivo"}), 403
            
        access_token = create_access_token(identity=str(usuario.id))
        return jsonify({
            "token": access_token,
            "usuario": usuario.to_dict()
        }), 200

    return jsonify({"msg": "Credenciales inválidas"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Con JWT stateless el logout se maneja usualmente en el cliente (borrando el token)
    # pero podemos retornar éxito para seguir el requerimiento.
    return jsonify({"msg": "Cierre de sesión exitoso"}), 200
