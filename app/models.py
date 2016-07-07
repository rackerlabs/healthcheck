from flask import jsonify
from . import db


class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(256), unique=True)
    email = db.Column('email', db.String(256), unique=True)
    description = db.Column('description', db.String(256), unique=True)
    dependencies = db.Column('dependencies', db.String(256), unique=True)

    # TABLE = tables.projects_table

    def __init__(self, name, email, description, dependencies, id=None):
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

    @staticmethod
    def get_projects():
        query = db.session.query(Projects)
        all_projects = query.all()
        projects_list = []
        for obj in all_projects:
            project = Projects(name=obj.name, email=obj.email, description=obj.description,
                               dependencies=obj.dependencies, id=obj.id)
            projects_list.append(project.to_json())
        return projects_list

    @staticmethod
    def new_project(post_request):
        name = post_request.get('name')

        if 'email' in post_request:
            email = post_request.get('email')
        else:
            email = None
        description = post_request.get('description')
        dependencies = post_request.get('dependencies')
        project = Projects(name, email, description, dependencies)
        db.session.add(project)
        db.session.commit()
        return project

    def get_tests(self):
        pass


    def delete_project(project):
      name = project.name
      db.session.delete(project)
      db.session.commit()
      message = "Deleted project '%s' " % name
      response = jsonify(message=message)
      response.status_code = 201
      return response



