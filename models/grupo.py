from db import db

class GrupoModel(db.Model):
    __tablename__ = 'grupos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    libro = db.Column(db.String(300))
    curso = db.Column(db.String(50))
    indicaciones = db.Column(db.String(300))
    
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesores.id'))

    alumnos_matriculados = db.relationship('AlumnoModel', secondary='matriculas', backref='grupos', lazy='dynamic')  

    def __init__(self, nombre, libro, curso, indicaciones, profesor_id):
        self.nombre = nombre
        self.libro = libro
        self.curso = curso
        self.indicaciones = indicaciones
        self.profesor_id = profesor_id
    
    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre, 
            'libro': self.libro,
            'curso': self.curso,
            'indicaciones': self.indicaciones,
            'profesor_id': self.profesor_id,
            'alumnos_matriculados': [alumno.json() for alumno in self.alumnos_matriculados.all()]
    }

    @classmethod
    def find_by_id(cls, id):
        return GrupoModel.query.filter_by(id=id).first()

    @classmethod
    def find_by_nombre(cls, nombre):
        return GrupoModel.query.filter_by(nombre=nombre).first()

    @classmethod
    def find_by_curso(cls, curso):
        return GrupoModel.query.filter_by(curso=curso)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()