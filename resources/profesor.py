from flask_restful import Resource, reqparse
from models.profesor import ProfesorModel


class ProfesorGenerico():
    parser = reqparse.RequestParser()
    parser.add_argument('id',
        type=int
    )
    parser.add_argument('nombre',
        type=str,
        required=True,
        help="El campo 'nombre' es obligatorio"
    )
    parser.add_argument('apellido1',
        type=str,
        required=True,
        help="El campo 'apellido1' es obligatorio"
    )
    parser.add_argument('apellido2',
        type=str
    )
    parser.add_argument('dni',
        type=str
    )
    parser.add_argument('telefono',
        type=str
    )
    parser.add_argument('email',
        type=str
    )
    parser.add_argument('direccion',
        type=str
    )


class Profesor(Resource, ProfesorGenerico):
    def get(self, id):
        profesor = ProfesorModel.find_by_id(id)
        if profesor:
            return profesor.json()
        return {'message': 'Profesor no encontrado'}, 404
    
    def put(self, id):
        data = Profesor.parser.parse_args()
        profesor = ProfesorModel.find_by_id(id)
        if profesor is None:
            return {'message': 'Profesor no encontrado. ¿Intentas modificar uno que no existe? '}, 404
        else:
            profesor.id = id
            profesor.nombre = data['nombre']
            profesor.apellido1 = data['apellido1']
            profesor.apellido2 = data['apellido2']
            profesor.dni = data['dni']        
            profesor.telefono = data['telefono']
            profesor.email = data['email']
            profesor.direccion = data['direccion']
            profesor.save_to_db()
            return profesor.json()
    
    def delete(self, id):
        profesor = ProfesorModel.find_by_id(id)
        if profesor:
            profesor.delete_from_db()
        return {'message':'Profesor borrado'}

class ProfesorNuevo(Resource, ProfesorGenerico):
    def post(self):
        data = ProfesorNuevo.parser.parse_args()
        if ProfesorModel.find_by_dni(data['dni']):
            return {'message': "A teacher with dni '{}' already exists.".format(data['dni'])}, 400 #Bad request    
        profesor = ProfesorModel(
                        data['nombre'], 
                        data['apellido1'], 
                        data['apellido2'], 
                        data['dni'], 
                        data['telefono'], 
                        data['email'], 
                        data['direccion']
        )
        try:
            profesor.save_to_db()
        except:
            return {"message": "An error occurred inserting profesor. "}, 500
        return profesor.json(), 201  

class ProfesoresList(Resource):
    def get(self):
        return {'profesores': [profesor.json() for profesor in ProfesorModel.query.all()]}