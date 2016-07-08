from flask import jsonify
from . import db


class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(256), unique=True)
    email = db.Column('email', db.String(256))
    description = db.Column('description', db.String(256))
    dependencies = db.Column('dependencies', db.String(256))

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
        return{
            'name': self.name,
            'email': self.email,
            'dependencies': self.dependencies,
            'description': self.description,
            'id': self.id
        }

    def get_project(self, id):
        query = db.session.query(Projects).get
        all_projects = query.all()
        projects_list = []
        for obj in all_projects:
            project = Projects(name=obj.name, email=obj.email, description=obj.description,
                               dependencies=obj.dependencies, id=obj.id)
            projects_list.append(project.to_json())
        return projects_list




