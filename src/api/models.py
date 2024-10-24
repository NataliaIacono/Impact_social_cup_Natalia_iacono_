from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    rol = db.Column(db.String, nullable=False)  # Ejemplo: "gerente" o "colaborador"

    tareas = db.relationship("Tarea", back_populates="usuario")
    colaboradores = db.relationship("Colaborador", back_populates="usuario")

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'tareas': [tarea.serialize() for tarea in self.tareas]  # Incluir tareas en la serialización
        }

    def __repr__(self):
        return f'<Usuario {self.nombre} - Rol {self.rol}>'
    
class Tarea(db.Model):
    __tablename__ = 'tareas'
    
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, default='pendiente')  # Ejemplo: 'pendiente', 'completada'
    fecha_vencimiento = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    usuario = db.relationship("Usuario", back_populates="tareas")

    def serialize(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'estado': self.estado,
            'fecha_vencimiento': self.fecha_vencimiento.isoformat(),  # Convertir a string
            'usuario_id': self.usuario_id,
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

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario = db.relationship("Usuario", back_populates="colaboradores")
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
