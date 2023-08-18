import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(250), nullable=False, unique=True)
    nombre = Column(String(250))
    apellido = Column(String(250))
    correo = Column(String(250), nullable=False, unique=True)
    contrasena = Column(String(250), nullable=False)
    publicaciones = relationship("Publicacion", back_populates="usuario")
    seguidores = relationship("Seguimiento", foreign_keys='Seguimiento.seguido_id', back_populates="seguido")
    siguiendo = relationship("Seguimiento", foreign_keys='Seguimiento.seguidor_id', back_populates="seguidor")

class Publicacion(Base):
    __tablename__ = 'publicacion'
    id = Column(Integer, primary_key=True)
    contenido = Column(String(500), nullable=False)
    fecha = Column(DateTime, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship("Usuario", back_populates="publicaciones")
    comentarios = relationship("Comentario", back_populates="publicacion")

class Comentario(Base):
    __tablename__ = 'comentario'
    id = Column(Integer, primary_key=True)
    contenido = Column(String(500), nullable=False)
    fecha = Column(DateTime, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship("Usuario")
    publicacion_id = Column(Integer, ForeignKey('publicacion.id'))
    publicacion = relationship("Publicacion", back_populates="comentarios")

class Seguimiento(Base):
    __tablename__ = 'seguimiento'
    id = Column(Integer, primary_key=True)
    seguidor_id = Column(Integer, ForeignKey('usuario.id'))
    seguidor = relationship("Usuario", foreign_keys=[seguidor_id], back_populates="siguiendo")
    seguido_id = Column(Integer, ForeignKey('usuario.id'))
    seguido = relationship("Usuario", foreign_keys=[seguido_id], back_populates="seguidores")

try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e


engine = create_engine('sqlite:///instagram.db')
Base.metadata.create_all(engine)
