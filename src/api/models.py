from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):  
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    contraseña = db.Column(db.String(500), unique=False, nullable=False)
    rol = db.Column(db.String, nullable=False)  # Ejemplo: "gerente" o "colaborador"

    tareas = db.relationship("Tarea", back_populates="user")  
    colaboradores = db.relationship("Colaborador", back_populates="user")  

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'tareas': [tarea.serialize() for tarea in self.tareas] 
        }

    def __repr__(self):
        return f'<User {self.nombre} - Rol {self.rol}>' 
    
class Tarea(db.Model):
    __tablename__ = 'tareas'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, default='pendiente')  
    fecha_vencimiento = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaboradores.id'), nullable=True)
    oportunidad_id = db.Column(db.Integer, db.ForeignKey('oportunidades.id'))  # Sigue siendo obligatorio

    user = db.relationship("User", back_populates="tareas")
    colaborador = db.relationship("Colaborador", back_populates="tareas")
    oportunidad = db.relationship("Oportunidad", back_populates="tareas")

    def serialize(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'estado': self.estado,
            'fecha_vencimiento': self.fecha_vencimiento.isoformat(),
            'user_id': self.user_id,
            'colaborador_id': self.colaborador_id,
            'oportunidad_id': self.oportunidad_id
        }

    def __repr__(self):
        return f'<Tarea {self.titulo} - Descripcion {self.descripcion} - Estado {self.estado}>'

class Oportunidad(db.Model):
    __tablename__ = 'oportunidades'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)  
    descripcion = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, default='disponible') 
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaboradores.id'))

    colaborador = db.relationship("Colaborador", back_populates="oportunidades")
    tareas = db.relationship("Tarea", back_populates="oportunidad", cascade="all, delete-orphan")

    def serialize(self):
        return {
            'id': self.id,
            'titulo': self.titulo,  
            'descripcion': self.descripcion,
            'estado': self.estado,
            'colaborador_id': self.colaborador_id,
            'tareas': [tarea.serialize() for tarea in self.tareas]
        }

    def __repr__(self):
        return f'<Oportunidad {self.titulo} - Estado {self.estado}>' 
    


class Colaborador(db.Model):
    __tablename__ = 'colaboradores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    rol = db.Column(db.String, default='colaborador')

    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))  
    user = db.relationship("User", back_populates="colaboradores")  
    oportunidades = db.relationship("Oportunidad", back_populates="colaborador")
    tareas = db.relationship("Tarea", back_populates="colaborador")

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'oportunidades': [oportunidad.serialize() for oportunidad in self.oportunidades],
            'tareas': [tarea.serialize() for tarea in self.tareas] 
        }

    def __repr__(self):
        return f'<Colaborador {self.nombre} - Rol {self.rol}>'


