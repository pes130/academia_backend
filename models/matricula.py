from db import db

""" If you want to use many-to-many relationships you will need to define a helper table that 
is used for the relationship. For this helper table it is strongly recommended to not use 
a model but an actual table """

class MatriculaModel(db.Model):
    __tablename__ = 'matriculas'
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), primary_key=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), primary_key=True)
    septiembre = db.Column(db.Float(precision=2))
    octubre = db.Column(db.Float(precision=2))
    noviembre = db.Column(db.Float(precision=2))
    diciembre = db.Column(db.Float(precision=2))
    enero = db.Column(db.Float(precision=2))
    febrero = db.Column(db.Float(precision=2))
    marzo = db.Column(db.Float(precision=2))
    abril = db.Column(db.Float(precision=2))
    mayo = db.Column(db.Float(precision=2))
    junio = db.Column(db.Float(precision=2))
    
    #alumno = db.relationship('AlumnoModel', backref="grupos_matriculados", cascade="all, delete-orphan",single_parent=True)
    #grupo = db.relationship('GrupoModel', backref="alumnos_matriculados", cascade="all, delete-orphan",single_parent=True)

    def __init__(self, alumno_id, grupo_id):
        self.alumno_id = alumno_id
        self.grupo_id = grupo_id
       
    @classmethod
    def find_by_id_alumno_grupo(cls, alumno_id, grupo_id):
        return MatriculaModel.query.filter_by(alumno_id=alumno_id).filter_by(grupo_id=grupo_id).first()
    
    def json(self):
        # devuelves un diccionario
        return {
            'alumno_id': self.alumno_id,
            'grupo_id': self.grupo_id,
            'septiembre': self.septiembre,
            'octubre': self.octubre,
            'noviembre': self.noviembre,
            'diciembre': self.diciembre,
            'enero': self.enero,
            'febrero': self.febrero,
            'marzo': self.marzo,
            'abril': self.abril,
            'mayo': self.mayo,
            'junio': self.junio
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()