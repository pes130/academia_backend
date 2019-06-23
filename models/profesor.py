from db import db

class ProfesorModel(db.Model):
    __tablename__ = 'profesores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido1 = db.Column(db.String(100))
    apellido2 = db.Column(db.String(100))
    dni = db.Column(db.String(9))
    telefono = db.Column(db.String(50))   
    email = db.Column(db.String(150))
    direccion = db.Column(db.String(300))

    grupos = db.relationship('GrupoModel', backref='profesor', lazy='dynamic') 

    def __init__(self, nombre, apellido1, apellido2, dni, telefono, email, direccion):
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.dni = dni
        self.telefono = telefono
        self.email = email
        self.direccion = direccion    
    
    def json(self):
        # devuelves un diccionario
        return {
            'id': self.id,
            'nombre': self.nombre, 
            'apellido1': self.apellido1,
            'apellido2': self.apellido2,
            'dni': self.dni,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'grupos': [grupo.json() for grupo in self.grupos.all()]
        }

    @classmethod
    def find_by_dni(cls, dni):
        return ProfesorModel.query.filter_by(dni=dni).first()
    
    @classmethod
    def find_by_id(cls, id):
        return ProfesorModel.query.filter_by(id=id).first()

    @classmethod
    def find_by_nombre(cls, nombre):
        return ProfesorModel.query.filter_by(nombre=nombre)
    
    @classmethod
    def find_by_apellido1(cls, apellido1):
        return ProfesorModel.query.filter_by(apellido1=apellido1)

    @classmethod
    def find_by_apellido2(cls, apellido2):
        return ProfesorModel.query.filter_by(apellido2=apellido2)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()