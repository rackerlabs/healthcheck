import unittest
import json
from app import create_app, db

data = {
    "status": "pass",
    "failure_details": ""
}

project_data = {
    'name': 'test project',
    'email': 'test@rackspace.com',
    'description': 'A test project',
    'dependencies': 'projectA'
}

canary_data = {
    "name": "test canary",
    "description": "OnMetal canary, tweet tweet",
    "meta_data": {
        "region": "Austin"
    },
    "criteria": {
        "expected_run_frequency": "5hrs",
        "threshold": "80%",
        "result_sample_size": 3
    }
}

expected_data = {
    "status": "pass",
    "failure_details": ""
}


class ResultTest(unittest.TestCase):
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
                                headers={'content-type': 'application/json'})

    def post_fake_canary(self):
        return self.client.post('/api/projects/1/canary',
                                data=json.dumps(canary_data),
                                headers={'content-type': 'application/json'})

    def post_fake_result(self):
        return self.client.post('/api/projects/1/canary/1/results',
                                data=json.dumps(data),
                                headers={'content-type': 'application/json'})

    @staticmethod
    def generate_fake_canary():
        from random import seed
        import forgery_py
        seed()
        data = {'name': forgery_py.lorem_ipsum.title(words_quantity=2),
                'description': forgery_py.lorem_ipsum.sentences(quantity=1, as_list=False),
                'meta_data': json.dumps(
                    {"region": forgery_py.lorem_ipsum.word()}),
                'criteria': json.dumps(
                    {'threshold': '90%', 'expected_run_frequency': '5hrs', 'result_sample_size': '10'})}
        return data

    @staticmethod
    def generate_fake_result():
        data = {'status' : 'pass',
                'failure_details' : ""
                }
        return data

    def test_post_result(self):
        project = self.post_fake_project()
        self.assertEquals(project.status_code, 201)
        self.assertEquals(json.loads(project.data).get('id'), 1)
        canary = self.post_fake_canary()
        self.assertEquals(canary.status_code, 201)
        self.assertEquals(json.loads(canary.data).get('id'), 1)
        result = self.post_fake_result()
        self.assertEquals(result.status_code, 201)
        json_data = json.loads(result.data)
        self.assertEquals(json_data.get('status'), 'pass', "result status does not match")
        self.assertEquals(json_data.get('id'), 1, "result id does not match")


    def test_get_result(self):
        project = self.post_fake_project()
        self.assertEquals(project.status_code, 201)
        self.assertEquals(json.loads(project.data).get('id'), 1)
        canary = self.post_fake_canary()
        self.assertEquals(canary.status_code, 201)
        self.assertEquals(json.loads(canary.data).get('id'), 1)
        result = self.post_fake_result()
        self.assertEquals(result.status_code, 201)
        self.assertEquals(json.loads(result.data).get('id'), 1)
        get_result = self.client.get('api/projects/1/canary/1/results/1', content_type='application/json')
        self.assertEquals(get_result.status_code, 200)
        json_data = json.loads(get_result.data)
        self.assertEquals(json_data.get('id'), 1, "Test_Get_Result: Result ID does not match")
        self.assertEquals(json_data.get('status'), 'pass', "Test_Get_Result : Result status does not match")


    def test_get_canaries(self):
        project = self.post_fake_project()
        self.assertEquals(project.status_code, 201)
        self.assertEquals(json.loads(project.data).get('id'), 1)
        canary = self.post_fake_canary()
        self.assertEquals(canary.status_code, 201)
        self.assertEquals(json.loads(canary.data).get('id'), 1)
        
        get_canary = self.client.get('api/projects/1/canary', content_type='application/json')
        self.assertEquals(get_canary.status_code, 200)
        # DO MORE CHECKS

    # def test_edit_canary(self):
    #     fake_project = self.post_fake_project()
    #     self.assertEquals(fake_project.status_code, 201)
    #     self.post_fake_canary()
    #     edit_response = self.client.put('api/projects/1/canary/1', data=json.dumps(
    #         {'criteria': {'threshold': '100%', 'expected_run_frequency': '5hrs', 'result_sample_size': '10'}}),
    #                                     headers={'content-type': 'application/json'})
    #
    #     self.assertEquals(edit_response.status_code, 200)
    #     response_data = json.loads(edit_response.data)
    #     self.assertEquals(response_data.get('criteria'),
    #                       {'threshold': '100%', 'expected_run_frequency': '5hrs', 'result_sample_size': '10'},
    #                       "EXPECTED {}, GOT {}".format({'threshold': '100%'}, response_data.get('criteria')))
    #
    # def test_delete_canary(self):
    #     fake_project = self.post_fake_project()
    #     self.assertEquals(fake_project.status_code, 201)
    #     self.post_fake_canary()
    #     delete_canary = self.client.delete('api/projects/1/canary/1')
    #     self.assertEquals(delete_canary.status_code, 200)  # disabled the canary
    #     get_canary = self.client.get('api/projects/1/canary/1', content_type='application/json')
    #     self.assertEquals(get_canary.status_code, 200)
    #     json_data = json.loads(get_canary.data)
    #     self.assertEquals(json_data.get('status'), "DISABLED", "ERROR : Canary not disabled")
