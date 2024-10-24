from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):  # Cambiado a User
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    rol = db.Column(db.String, nullable=False)  # Ejemplo: "gerente" o "colaborador"

    tareas = db.relationship("Tarea", back_populates="user")  # Actualizado a "user"
    colaboradores = db.relationship("Colaborador", back_populates="user")  # Actualizado a "user"

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'tareas': [tarea.serialize() for tarea in self.tareas]  # Incluir tareas en la serialización
        }

    def __repr__(self):
        return f'<User {self.nombre} - Rol {self.rol}>'  # Actualizado a User
    
class Tarea(db.Model):
    __tablename__ = 'tareas'
    
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, default='pendiente')  # Ejemplo: 'pendiente', 'completada'
    fecha_vencimiento = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))  # Actualizado a 'user_id'

    user = db.relationship("User", back_populates="tareas")  # Actualizado a "User"

    def serialize(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'estado': self.estado,
            'fecha_vencimiento': self.fecha_vencimiento.isoformat(),  # Convertir a string
            'user_id': self.user_id,  # Actualizado a "user_id"
        }

    def __repr__(self):
        return f'<Tarea {self.descripcion} - Estado {self.estado}>'

class Oportunidad(db.Model):
    __tablename__ = 'oportunidades'
    
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, default='disponible')  # Ejemplo: 'disponible', 'ocupada'
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaboradores.id'))

    colaborador = db.relationship("Colaborador", back_populates="oportunidades")

    def serialize(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'estado': self.estado,
            'colaborador_id': self.colaborador_id,
        }

    def __repr__(self):
        return f'<Oportunidad {self.descripcion} - Estado {self.estado}>'

class Colaborador(db.Model):
    __tablename__ = 'colaboradores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    rol = db.Column(db.String, default='colaborador')

    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))  # Actualizado a 'user_id'
    user = db.relationship("User", back_populates="colaboradores")  # Actualizado a "User"
    oportunidades = db.relationship("Oportunidad", back_populates="colaborador")

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'oportunidades': [oportunidad.serialize() for oportunidad in self.oportunidades]
        }

    def __repr__(self):
        return f'<Colaborador {self.nombre} - Rol {self.rol}>'
