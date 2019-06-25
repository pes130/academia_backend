from flask_restful import Resource, reqparse
from models.grupo import GrupoModel
from flask_jwt_extended import jwt_required, fresh_jwt_required


class GrupoGenerico:
    parser = reqparse.RequestParser()
    parser.add_argument('id',
        type=int
    )
    parser.add_argument('nombre',
        type=str,
        required=True,
        help="El campo 'nombre' es obligatorio"
    )
    parser.add_argument('libro',
        type=str
    )
    parser.add_argument('curso',
        type=str,
        required=True,
        help="El campo 'curso' es obligatorio"
    )
    parser.add_argument('indicaciones',
        type=str
    )
    parser.add_argument('profesor_id',
        type=int
    )

class Grupo(Resource, GrupoGenerico):
    @jwt_required
    def get(self, id):
        grupo = GrupoModel.find_by_id(id)
        if grupo:
            return grupo.json()
        return {'message': 'Grupo no encontrado'}, 404

    @fresh_jwt_required
    def put(self, id):
        data = Grupo.parser.parse_args()
        grupo = GrupoModel.find_by_id(id)
        if grupo is None:
            return {'message': 'Grupo no encontrado. ¿Intentas modificar uno que no existe? '}, 404
        else:
            grupo.id = id
            grupo.nombre = data['nombre']
            grupo.libro = data['libro']
            grupo.curso = data['curso']
            grupo.indicaciones = data['indicaciones']  
            grupo.profesor_id = data['profesor_id']      
            grupo.save_to_db()
            return grupo.json()

    @fresh_jwt_required
    def delete(self, id):
        grupo = GrupoModel.find_by_id(id)
        if grupo:
            grupo.delete_from_db()
        return {'message':'Grupo borrado'}

    
class GrupoNuevo(Resource, GrupoGenerico):
    
    @fresh_jwt_required
    def post(self):
        data = GrupoNuevo.parser.parse_args()
        grupo = GrupoModel.find_by_nombre(data['nombre'])
        if grupo is not None:
            return {'message': "Un grupo con el nombre '{}' ya existe.".format(data['nombre'])}, 400 #Bad request    
        grupo = GrupoModel(
                        data['nombre'], 
                        data['libro'], 
                        data['curso'], 
                        data['indicaciones'],
                        data['profesor_id']
        )
        try:
            grupo.save_to_db()
        except:
            return {"message": "An error occurred inserting grupo. "}, 500
        return grupo.json(), 201  
    

class GruposList(Resource):
    @jwt_required
    def get(self, curso=None):
        if not curso:
            return {'grupos': [grupo.json() for grupo in GrupoModel.query.all()]}
        else:
            grupos = GrupoModel.find_by_curso(curso)
            return {'grupos': [grupo.json() for grupo in grupos.all()]}