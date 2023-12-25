import os
from sqlalchemy import Column, String, Integer, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

database_path = "postgresql://postgres:1234567890@fsnd-db.cud9wfdw2uig.us-east-2.rds.amazonaws.com:5432/fsnd_db"
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_for_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_for_db(app, database_path=database_path):
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    db.app = app
    app.app_context().push()
    db.init_app(app)
    db.create_all()


'''
Class for Movie
'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    actors = relationship('Actor', backref="movie", lazy=True)
    release_date = Column(String)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


'''
Class for Actor
'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    gender = Column(String)
    name = Column(String)
    age = Column(Integer)
    
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=True)

    def __init__(self, name, age, gender, movie_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.movie_id = movie_id

    def insert(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


    def format(self):
        return {
            'id': self.id,
            'gender': self.gender,
            'name': self.name,
            'age': self.age,
            'movie_id': self.movie_id
        }