import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
# from resources.user import UserRegister
from resources.alumno import Alumno, AlumnosList, AlumnoNuevo
from resources.profesor import Profesor, ProfesoresList, ProfesorNuevo
from resources.grupo import Grupo, GruposList, GrupoNuevo
from resources.matricula import Matricula, MatriculasList, MatriculaNueva

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite://data.db')
#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://useracademiadb:useracademiadb@localhost/academiadb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#ueremos que alchemy nos cree las tablas
@app.before_first_request
def create_tables():
    db.create_all()

app.secret_key = 'pablo'


# Nos permite asociar facilmente recursos a métodos.
api = Api(app)
# jwt = JWT(app, authenticate, identity)
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
# api.add_resource(UserRegister,'/register')
# api.add_resource(Store,'/store/<string:name>')
# api.add_resource(StoreList,'/stores')


# Con uWSGI no pasas por aquí, así que no importas db
if __name__ == '__main__':
    # Imports circulares, si importamos db al princpio, y en models también vas a crear una importación circular
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)