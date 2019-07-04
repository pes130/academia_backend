import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import User, UserRegister, UserLogin, TokenRefresh, TokenExpire
from resources.alumno import Alumno, AlumnosList, AlumnoNuevo
from resources.profesor import Profesor, ProfesoresList, ProfesorNuevo
from resources.grupo import Grupo, GruposList, GrupoNuevo
from resources.matricula import Matricula, MatriculasList, MatriculaNueva
from resources.uploads import UploadImage
from security import authenticate, identity
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite://data.db')
# TODO lee esto de una variable de entorno
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://useracademiadb:useracademiadb@localhost/academiadb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

#ueremos que alchemy nos cree las tablas
@app.before_first_request
def create_tables():
    db.create_all()
# TODO leer esto de una variable de entorno
app.secret_key = 's3cr3ti110_12345*'


# Nos permite asociar facilmente recursos a métodos.
api = Api(app)
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return TokenExpire.is_token_expired(jti)


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {
            "description": "Token has expired!",
            "error": "token_expired"
    }), 401
    

@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify(
        {
            "description": "Signature verification failed!",
            "error": "invalid_token"
    }), 401
    


@jwt.unauthorized_loader
def unauthorized_loader_callback(error):
    return jsonify(
        {
            "description": "Access token not found!",
            "error": "unauthorized_loader"
    }), 401
    


@jwt.needs_fresh_token_loader
def fresh_token_loader_callback():
    return jsonify(
        {
            "description": "Token is not fresh. Fresh token needed!",
            "error": "needs_fresh_token",
            "code": 401
    }), 401

api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserRegister, "/auth/register")
api.add_resource(UserLogin, "/auth/login")
api.add_resource(TokenRefresh, "/auth/refresh")
api.add_resource(TokenExpire, "/auth/logout")


api.add_resource(Alumno,'/alumno/<int:id>')
api.add_resource(AlumnoNuevo,'/alumno')
api.add_resource(AlumnosList,'/alumnos')
api.add_resource(Profesor,'/profesor/<int:id>')
api.add_resource(ProfesorNuevo,'/profesor')
api.add_resource(ProfesoresList,'/profesores')
api.add_resource(Grupo,'/grupo/<int:id>')
api.add_resource(GrupoNuevo,'/grupo')
api.add_resource(GruposList,'/grupos','/grupos/<string:curso>')
api.add_resource(Matricula,'/matricula/<int:grupo_id>/<int:alumno_id>')
api.add_resource(MatriculasList,'/matriculas')
api.add_resource(MatriculaNueva,'/matricula')
api.add_resource(UploadImage,'/upload/image')





# Con uWSGI no pasas por aquí, así que no importas db
if __name__ == '__main__':
    # Imports circulares, si importamos db al princpio, y en models también vas a crear una importación circular
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)