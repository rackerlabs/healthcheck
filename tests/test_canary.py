import unittest
import json
from healthcheck import create_app, db

header = {'content-type': 'application/json'}
content_type = 'application/json'
data = {'name': 'test canary',
        'description': 'A test canary',
        'meta_data': {'region': 'Hong Kong', 'data2': 'tweete'},
        'criteria': {'threshold': '90%',
                     'expected_run_frequency': '5hrs',
                     'result_sample_size': '10'}
        }

project_data = {'name': 'test project',
                'email': 'test@rackspace.com',
                'description': 'A test project',
                'dependencies': 'projectA'}

expected_data = {'name': 'test canary',
                 'description': 'A test canary',
                 'meta_data': {'region': 'Hong Kong', 'data2': 'tweete'},
                 'status': 'ACTIVE',
                 'health': 'GREEN',
                 'criteria': {'threshold': '90%',
                              'expected_run_frequency': '5hrs',
                              'result_sample_size': '10'},
                 'id': 1
                 }


class CanaryTest(unittest.TestCase):
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

    def post_fake_project(self):
        return self.client.post('/api/projects',
                                data=json.dumps(project_data),
                                headers=header)

    def post_fake_canary(self):
        return self.client.post('/api/projects/1/canary',
                                data=json.dumps(data),
                                headers=header)

    def fake_canary(self):
        return self.client.post('/api/projects/1/canary',
                                data=json.dumps(self.generate_fake_canary()),
                                headers=header)

    @staticmethod
    def generate_fake_canary():
        from random import seed
        import forgery_py
        seed()
        data = {'name': forgery_py.lorem_ipsum.title(words_quantity=2),
                'description': forgery_py.lorem_ipsum.sentences(quantity=1,
                                                                as_list=False),
                'meta_data': json.dumps(
                    {"region": forgery_py.lorem_ipsum.word()}),
                'criteria': json.dumps(
                    {'threshold': '90%', 'expected_run_frequency': '5hrs',
                     'result_sample_size': '10'})}
        return data

    def test_post_canary(self):
        canary_project = self.post_fake_project()
        self.assertEquals(canary_project.status_code, 201)
        self.assertEquals(json.loads(canary_project.data).get('id'), 1)
        post_canary = self.post_fake_canary()
        self.assertEquals(post_canary.status_code, 201)
        json_data = json.loads(post_canary.data)
        self.assertEquals(sorted(json_data.items()),
                          sorted(expected_data.items()),
                          "EXPECTED {}, GOT {}".format(expected_data,
                                                       json_data))

    def test_get_canary(self):
        fake_project = self.post_fake_project()
        self.assertEquals(fake_project.status_code, 201)
        self.assertEquals(json.loads(fake_project.data).get('id'), 1)
        post_canary = self.post_fake_canary()
        self.assertEquals(post_canary.status_code, 201)
        get_canary = self.client.get('api/projects/1/canary/1',
                                     content_type=content_type)
        self.assertEquals(get_canary.status_code, 200)
        json_data = json.loads(get_canary.data)
        self.assertEquals(sorted(json_data.items()),
                          sorted(expected_data.items()),
                          "EXPECTED {}, GOT {}".format(expected_data,
                                                       json_data))

    def test_get_canaries(self):
        fake_project = self.post_fake_project()
        self.assertEquals(fake_project.status_code, 201)
        self.fake_canary()
        self.fake_canary()
        get_canary = self.client.get('api/projects/1/canary',
                                     content_type=content_type)
        self.assertEquals(get_canary.status_code, 200)

    def test_edit_canary(self):
        fake_project = self.post_fake_project()
        self.assertEquals(fake_project.status_code, 201)
        self.post_fake_canary()
        expected_data = {"criteria": {'threshold': '100%',
                                      'expected_run_frequency': '5hrs',
                                      'result_sample_size': '10'}}
        edit_response = self.client.put('api/projects/1/canary/1',
                                        data=json.dumps(expected_data),
                                        headers=header)

        self.assertEquals(edit_response.status_code, 200)
        response_data = json.loads(edit_response.data)
        self.assertEquals(response_data.get('criteria'),
                          expected_data.get('criteria'),
                          "EXPECTED {}, GOT {}".format({'threshold': '100%'},
                                                       response_data.get(
                                                           'criteria')))

    def test_delete_canary(self):
        fake_project = self.post_fake_project()
        self.assertEquals(fake_project.status_code, 201)
        self.post_fake_canary()
        delete_canary = self.client.delete('api/projects/1/canary/1')
        self.assertEquals(delete_canary.status_code, 200)
        get_canary = self.client.get('api/projects/1/canary/1',
                                     content_type=content_type)
        self.assertEquals(get_canary.status_code, 200)
        json_data = json.loads(get_canary.data)
        self.assertEquals(json_data.get('status'), "DISABLED",
                          "ERROR : Canary not disabled")
