from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db, bcrypt, Usuario
from routes.auth import auth_bp
from routes.usuarios import usuarios_bp
import os

app = Flask(__name__)

# Configuración
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'localxplore-secret-key-2024' # Cambiar en producción

# Inicialización
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Registro de Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')

def init_db():
    with app.app_context():
        db.create_all()
        
        # Crear admin si no existe
        admin_email = "admin@localxplore.com"
        if not Usuario.query.filter_by(email=admin_email).first():
            admin = Usuario(
                nombre="Administrador",
                apellido="LocalXplore",
                email=admin_email,
                rol="admin",
                estado=True
            )
            admin.set_password("Admin123!")
            db.session.add(admin)
            db.session.commit()
            print("Admin inicial creado: admin@localxplore.com / Admin123!")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
