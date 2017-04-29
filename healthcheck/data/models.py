import copy

from healthcheck import db
from flask import json
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(256), unique=True)
    email = db.Column('email', db.String(256))
    description = db.Column('description', db.String(256))
    dependencies = db.Column('dependencies', db.String(256))
    canaries = db.relationship('Canary', backref='project', lazy='dynamic')

    def __init__(self, name, email, description=None,
                 dependencies=None, id=None):
        self.name = name
        self.email = email
        self.description = description
        self.dependencies = dependencies
        self.id = id

    def __repr__(self):
        return "[name = '%s', email= '%s', " \
               "description= '%s', dependencies= '%s']" \
               % (self.name, self.email, self.description, self.dependencies)

    def project_to_json(self):
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
    meta_data = db.Column('data', JSON)
    status = db.Column('status', db.String(256))
    criteria = db.Column('criteria', JSON)
    health = db.Column('health', db.String(256))
    updated_at = db.Column('updated_at', db.DateTime())
    history = db.Column('history', JSON)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    results = db.relationship('Results', backref='canary', lazy='dynamic')

    def __init__(self, name, description=None, meta_data=None,
                 status='ACTIVE', criteria=None, health='GREEN',
                 updated_at=None, id=None, project_id=project_id):
        self.name = name
        self.description = description
        self.meta_data = meta_data
        self.status = status
        self.criteria = criteria
        self.health = health
        self.history = {"{}".format(datetime.utcnow()): health}
        self.updated_at = updated_at or datetime.utcnow()
        self.id = id
        self.project_id = project_id

    def update_health(self, new_health):
        if new_health and new_health != self.health:
            self.health = new_health
            self.updated_at = datetime.utcnow()
            new_history = copy.deepcopy(self.history)
            new_history["{}".format(datetime.utcnow())] = new_health
            self.history = new_history

    def canary_to_json(self):
        return {
            'name': self.name,
            'description': self.description,
            'meta_data': self.meta_data,
            'status': self.status,
            'criteria': self.criteria,
            'health': self.health,
            'updated_at': self.updated_at,
            'history': self.history,
            'id': self.id
        }


class Results(db.Model):
    __tablename__ = 'results'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    status = db.Column('status', db.String(256))
    failure_details = db.Column('failure_details', db.String(256))
    created_at = db.Column('created_at', db.DateTime())
    canary_id = db.Column(db.Integer, db.ForeignKey('canaries.id'))

    def __init__(self, status=status, created_at=None,
                 failure_details=None, id=None,
                 canary_id=canary_id):
        self.status = status
        self.failure_details = failure_details
        self.created_at = created_at or datetime.utcnow()
        self.id = id
        self.canary_id = canary_id

    def results_to_json(self):
        return {
            'status': self.status,
            'failure_details': self.failure_details,
            'created_at': "{}".format(self.created_at),
            'id': self.id

        }
