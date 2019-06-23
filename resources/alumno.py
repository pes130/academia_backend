from flask_restful import Resource, reqparse
from models.alumno import AlumnoModel
from datetime import datetime


class AlumnoRequestGenerico:
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
        type=str,
        required=True
    )
    parser.add_argument('dni',
        type=str,
        required=True,
        help="El campo 'dni' es obligatorio"
    )
    parser.add_argument('f_nacimiento',
        type=str,
        required=True,
        help="El campo 'f_nacimiento' es obligatorio"
    )
    parser.add_argument('madre',
        type=str
    )
    parser.add_argument('padre',
        type=str
    )
    parser.add_argument('telefono_padre',
        type=str
    )
    parser.add_argument('telefono_madre',
        type=str
    )
    parser.add_argument('alergias',
        type=str
    )
    parser.add_argument('observaciones',
        type=str
    )
    parser.add_argument('domiciliacion',
        type=str
    )

# Request para paths al que se le añade el id del alumno
class Alumno(AlumnoRequestGenerico, Resource): 
    def get(self, id):
        alumno = AlumnoModel.find_by_id(id)
        if alumno:
            return alumno.json()
        return {'message': 'Alumno no encontrado'}, 404

    def put(self, id):
        data = Alumno.parser.parse_args()
        alumno = AlumnoModel.find_by_id(id)
        if alumno is None:
            return {'message': 'Alumno no encontrado. ¿Intentas modificar uno que no existe? '}, 404
        else:
            alumno.nombre = data['nombre']
            alumno.apellido1 = data['apellido1']
            alumno.apellido2 = data['apellido2']
            alumno.dni = data['dni']
            f_nacimiento = datetime.strptime(data['f_nacimiento'], '%d/%m/%Y')
            alumno.f_nacimiento = f_nacimiento
            alumno.madre = data['madre']
            alumno.padre = data['padre']
            alumno.telefono_padre = data['telefono_padre']
            alumno.telefono_madre = data['telefono_madre']
            alumno.alergias = data['alergias']
            alumno.observaciones = data['observaciones']
            alumno.domiciliacion = data['domiciliacion']
            alumno.save_to_db()
            return alumno.json()

    def delete(self, id):
        alumno = AlumnoModel.find_by_id(id)
        if alumno:
            alumno.delete_from_db()
        return {'message':'Alumno borrado'}

# Para los alumnos nuevos no sabemos su id, así que creamos un recurso nuevo
class AlumnoNuevo(AlumnoRequestGenerico, Resource):
    def post(self):
        data = AlumnoNuevo.parser.parse_args()
        if AlumnoModel.find_by_dni(data['dni']):
            return {'message': "A student with dni '{}' already exists.".format(data['dni'])}, 400 #Bad request 
        f_nacimiento = datetime.strptime(data['f_nacimiento'], '%d/%m/%Y')
        alumno = AlumnoModel(data['nombre'], data['apellido1'], data['apellido2'], 
                        data['dni'], f_nacimiento, data['madre'], data['padre'], 
                        data['telefono_padre'], data['telefono_madre'],data['alergias'], data['observaciones'], data['domiciliacion']) 
        try:
            alumno.save_to_db()
        except:
        # except Exception as e:
            # if hasattr(e, 'message'):
            #     print(e.message)
            # else:
            #     print(e)
            return {"message": "An error occurred inserting alumno. "}, 500
        return alumno.json(), 201  
    

class AlumnosList(Resource):
    def get(self):
        return {'alumnos': [alumno.json() for alumno in AlumnoModel.query.all()]}