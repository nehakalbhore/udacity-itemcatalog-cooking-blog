#!/usr/bin/env python

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine(
    'sqlite:///rb.db', connect_args={'check_same_thread': False})


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    email = Column(String, index=True)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }


class Cuisine(Base):
    __tablename__ = 'cuisine'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    ingredients = Column(String(4096))
    body = Column(String(4096 * 4), nullable=False)
    created = Column(Date, nullable=False)
    cuisine_id = Column(Integer, ForeignKey('cuisine.id'))
    cuisine = relationship(Cuisine)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
            'body': self.body,
            'created': self.created.isoformat(),
            'cuisine': self.cuisine.serialize,
            'user': self.user.serialize
        }


Base.metadata.create_all(engine)
