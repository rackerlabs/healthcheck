from flask import jsonify, json
from flask import current_app
from sqlalchemy.dialects.postgresql import JSON
from . import db



class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(256), unique=True)
    email = db.Column('email', db.String(256))
    description = db.Column('description', db.String(256))
    dependencies = db.Column('dependencies', db.String(256))
    canaries = db.relationship('Canary', backref='project', lazy='dynamic')

    def __init__(self, name, email, description=None, dependencies=None, id=None):
        self.name = name
        self.email = email
        self.description = description
        self.dependencies = dependencies
        self.id = id

    def __repr__(self):
        return "[name = '%s', email= '%s', description= '%s', dependencies= '%s']" % (self.name, self.email,
                                                                                      self.description,
                                                                                      self.dependencies)

    def to_json(self):
        return {
            'name': self.name,
            'email': self.email,
            'dependencies': self.dependencies,
            'description': self.description,
            'id': self.id
        }

    def get_canary(self, canary_id):
        canary = Canary.query.get(canary_id)
        if canary is None:
            return 'canary_id not found'
        return canary


class Canary(db.Model):
    __tablename__ = 'canaries'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(256), unique=True)
    description = db.Column('description', db.String(256))
    data = db.Column(JSON)
    criteria = db.Column(JSON)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, name, criteria, data=None, description=None, id=None):
        self.name = name
        self.description = description
        self.data = data
        self.criteria = criteria
        self.id = id

    def canary_to_json(self):
        return {
            'name': self.name,
            'description': self.description,
            'data': self.data,
            'criteria': self.criteria,
            'id': self.id
        }



