import unittest
import json
from app import create_app, db
from app.models import Projects

data = {'name': 'test project',
        'email': 'test@rackspace.com',
        'description': 'A test project',
        'dependencies': 'projectA'}


class ProjectsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def helper_post(self):
        return self.client.post('/api/projects',
                                data=json.dumps(data),
                                headers={'content-type': 'application/json'})

    @staticmethod
    def generate_fake(count):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        all_projects = []
        seed()
        for i in range(count):
            u = Projects(name=forgery_py.lorem_ipsum.title(words_quantity=2), email=forgery_py.internet.email_address(),
                         description=forgery_py.lorem_ipsum.sentences(quantity=1, as_list=False),
                         dependencies="project " + forgery_py.lorem_ipsum.word())

            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:  # WHAT HAPPENS IF THE ERROR HAPPENED HERE
                db.session.rollback()
            all_projects.append(u)

        if len(all_projects) != count:
            print "ERROR : Number of projects in database is less than count "
            # maybe return here??
        return all_projects

    def test_post_project(self):
        post_response = self.helper_post()
        self.assertEquals(post_response.status_code, 201)
        json_data = json.loads(post_response.data)
        expected = dict(id=1, name='test project')
        self.assertEquals(json_data, expected,
                          "expected 1 and test project but got {} and {}".format(json_data.get('id'),
                                                                                 json_data.get('name')))

    def test_get_projects(self):
        num = 2
        fake_projects = self.generate_fake(num)
        get_response = self.client.get('api/projects', content_type='application/json')
        self.assertEqual(get_response.status_code, 200)
        projects_list = json.loads(get_response.data).get('projects')
        for i in range(num):
            self.assertEquals((projects_list[i].get('id')), fake_projects[i].id, "project id does not match")
            self.assertEquals((projects_list[i].get('name')), fake_projects[i].name, "project name does not match")
            self.assertEquals((projects_list[i].get('email')), fake_projects[i].email, "project email does not match")
            self.assertEquals((projects_list[i].get('description')), fake_projects[i].description,
                              "project description does not match")
            self.assertEquals((projects_list[i].get('dependencies')), fake_projects[i].dependencies,
                              "project dependencies does not match")

    def test_get_project(self):
        self.helper_post()
        get_response = self.client.get('api/projects/1', content_type='application/json')
        self.assertEquals(get_response.status_code, 200)
        json_data = json.loads(get_response.data)
        self.assertEquals(json_data.get('id'), 1, "project id does not match")
        self.assertEquals(json_data.get('name'), data.get('name'), "project name does not match")
        self.assertEquals(json_data.get('email'), data.get('email'), "project email does not match")
        self.assertEquals(json_data.get('description'), data.get('description'), "project description does not match")
        self.assertEquals(json_data.get('dependencies'), data.get('dependencies'),
                          "project dependencies does not match")
        # WON'T HAVE THESE 4 LINES BUT FOR THE ALPHABETICAL ORDER ISSUE

    def test_put_project(self):
        self.helper_post()
        put_response = self.client.put('api/projects/1', data=json.dumps({'name': 'new project'}),
                                       headers={'content-type': 'application/json'})
        self.assertEquals(put_response.status_code, 200)
        response_data = json.loads(put_response.data)
        self.assertEquals(response_data.get('name'), 'new project',
                          "Expected 'new project', got {}".format(response_data.get('name')))

    def test_delete_project(self):
        self.helper_post()
        del_response = self.client.delete('api/projects/1')
        self.assertEquals(del_response.status_code, 200)
        expected = "Deleted project test project"
        self.assertEquals(json.loads(del_response.data).get('message'), expected)

        #     #WHAT HAPPENS ON BAD URL?


if __name__ == '__main__':
    unittest.main()
