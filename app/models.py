from sqlalchemy.dialects.postgresql import *
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


class Canary(db.Model):
    __tablename__ = 'canaries'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(256), unique=True)
    description = db.Column('description', db.String(256))
    data = db.Column('data', JSON)
    status = db.Column('status', db.String(256))
    criteria = db.Column('criteria', JSON)
    health = db.Column('health', db.String(256))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, name, description=None, data=None, status='ACTIVE', criteria=None, health='GREEN', id=None,
                 project_id=project_id):
        self.name = name
        self.description = description
        self.data = data
        self.status = status
        self.criteria = criteria
        self.health = health
        self.id = id
        self.project_id = project_id

    def canary_to_json(self):
        return {
            'name': self.name,
            'description': self.description,
            'data': self.data,
            'status': self.status,
            'criteria': self.criteria,
            'health': self.health,
            'id': self.id

        }
