from flask_restful import Resource, reqparse
from models.matricula import MatriculaModel


class MatriculaGenerica():
    parser = reqparse.RequestParser()
    parser.add_argument('alumno_id',
        type=int,
        required=True,
        help="El campo 'alumno_id' es obligatorio"
    )
    parser.add_argument('grupo_id',
        type=int,
        required=True,
        help="El campo 'grupo_id' es obligatorio"
    )
    parser.add_argument('activa',
        type=bool
    )
    parser.add_argument('septiembre',
        type=float
    )
    parser.add_argument('octubre',
        type=float
    )
    parser.add_argument('noviembre',
        type=float
    )
    parser.add_argument('diciembre',
        type=float
    )
    parser.add_argument('enero',
        type=float
    )
    parser.add_argument('febrero',
        type=float
    )
    parser.add_argument('marzo',
        type=float
    )
    parser.add_argument('abril',
        type=float
    )
    parser.add_argument('mayo',
        type=float
    )
    parser.add_argument('junio',
        type=float
    )

class Matricula(Resource, MatriculaGenerica):
    def get(self, grupo_id, alumno_id):
        matricula = MatriculaModel.find_by_id_alumno_grupo(alumno_id, grupo_id)
        if matricula:
            return matricula.json()
        return {'message': 'Matrícula no encontrada'}, 404

    def delete(self, grupo_id, alumno_id):
        matricula = MatriculaModel.find_by_id_alumno_grupo(alumno_id, grupo_id)
        if matricula:
            matricula.delete_from_db()
        return {'message':'Matricula borrada'}


    def put(self, grupo_id, alumno_id):
        data = Matricula.parser.parse_args()
        matricula = MatriculaModel.find_by_id_alumno_grupo(alumno_id, grupo_id)
        if matricula is None:
            return {'message': 'Matrícula de alumno no encontrada '}, 404
        else:
            matricula.activa = data['activa']
            matricula.septiembre = data['septiembre']
            matricula.octubre = data['octubre']
            matricula.noviembre = data['noviembre']
            matricula.diciembre = data['diciembre']
            matricula.enero = data['enero']
            matricula.febrero = data['febrero']
            matricula.marzo = data['marzo']
            matricula.abril = data['abril']
            matricula.mayo = data['mayo']
            matricula.junio = data['junio']     
            matricula.save_to_db()
            return matricula.json()


class MatriculaNueva(Resource, MatriculaGenerica):
    def post(self):
        data = MatriculaNueva.parser.parse_args()

        matricula = MatriculaModel.find_by_id_alumno_grupo(data['alumno_id'],data['grupo_id'])
        if matricula is not None:
            return {'message': "Alumno ya matriculado en ese curso"}, 400 #Bad request    
        matricula = MatriculaModel(
                        data['alumno_id'],
                        data['grupo_id']
        )
        try:
            matricula.save_to_db()
        except:
            return {"message": "Ocurrió un error matriculando al alumno en el grupo. "}, 500
        return matricula.json(), 201      


class MatriculasList(Resource):
    def get(self):
        return {'matriculas': [matricula.json() for matricula in MatriculaModel.query.all()]}




    
