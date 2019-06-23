from db import db
from datetime import datetime

class AlumnoModel(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido1 = db.Column(db.String(100))
    apellido2 = db.Column(db.String(100))
    dni = db.Column(db.String(9))
    f_nacimiento = db.Column(db.DateTime)
    madre = db.Column(db.String(200))
    padre = db.Column(db.String(200))
    telefono_padre = db.Column(db.String(100))
    telefono_madre = db.Column(db.String(100))
    alergias = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    domiciliacion = db.Column(db.String(100))

    grupos_matriculados = db.relationship('MatriculaModel', backref='alumno', lazy='dynamic') 

    def __init__(self, nombre, apellido1, apellido2, dni, f_nacimiento, madre, padre, telefono_padre, 
            telefono_madre, alergias, observaciones, domiciliacion):
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.dni = dni
        self.f_nacimiento = f_nacimiento
        self.madre = madre
        self.padre = padre
        self.telefono_padre = telefono_padre
        self.telefono_madre = telefono_madre
        self.alergias = alergias
        self.observaciones = observaciones
        self.domiciliacion = domiciliacion
    
    def json(self):
        # devuelves un diccionario
        return {
            'id': self.id,
            'nombre': self.nombre, 
            'apellido1': self.apellido1,
            'apellido2': self.apellido2,
            'dni': self.dni,
            'f_nacimiento': self.f_nacimiento.strftime('%d/%m/%Y'),
            'madre': self.madre,
            'padre': self.padre,
            'telefono_padre': self.telefono_padre,
            'telefono_madre': self.telefono_madre,
            'alergias': self.alergias,
            'observaciones': self.observaciones,
            'domiciliacion': self.domiciliacion,
        }

    @classmethod
    def find_by_dni(cls, dni):
        return AlumnoModel.query.filter_by(dni=dni).first()
    
    @classmethod
    def find_by_id(cls, id):
        return AlumnoModel.query.filter_by(id=id).first()

    @classmethod
    def find_by_nombre(cls, nombre):
        return AlumnoModel.query.filter_by(nombre=nombre)
    
    @classmethod
    def find_by_apellido1(cls, apellido1):
        return AlumnoModel.query.filter_by(apellido1=apellido1)

    @classmethod
    def find_by_apellido2(cls, apellido2):
        return AlumnoModel.query.filter_by(apellido2=apellido2)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()