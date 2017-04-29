import unittest
import json
from healthcheck import create_app, db


header = {'content-type': 'application/json'}
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
        project = self.post_fake_project()
        self.assertEquals(project.status_code, 201)
        self.assertEquals(json.loads(project.data).get('id'), 1)
        canary = self.post_fake_canary()
        self.assertEquals(canary.status_code, 201)
        self.assertEquals(json.loads(canary.data).get('id'), 1)

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
                                data=json.dumps(canary_data),
                                headers=header)

    def post_fake_result(self):
        return self.client.post('/api/projects/1/canary/1/results',
                                data=json.dumps(data),
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

    @staticmethod
    def generate_fake_result():
        data = {'status': 'pass',
                'failure_details': ""
                }
        return data

    def test_post_result(self):
        result = self.post_fake_result()
        self.assertEquals(result.status_code, 201)
        json_data = json.loads(result.data)
        self.assertEquals(json_data.get('status'), 'pass',
                          "result status does not match")
        self.assertEquals(json_data.get('id'), 1, "result id does not match")

    def test_get_result(self):
        result = self.post_fake_result()
        self.assertEquals(result.status_code, 201)
        self.assertEquals(json.loads(result.data).get('id'), 1)
        get_result = self.client.get('api/projects/1/canary/1/results/1',
                                     content_type='application/json')
        self.assertEquals(get_result.status_code, 200)
        json_data = json.loads(get_result.data)
        self.assertEquals(json_data.get('id'), 1,
                          "Test_Get_Result: Result ID does not match")
        self.assertEquals(json_data.get('status'), 'pass',
                          "Test_Get_Result : Result status does not match")

    def test_get_results(self):
        results = 3
        for i in range(0, results):
            self.post_fake_result()
        get_canary = self.client.get('api/projects/1/canary/1/results',
                                     content_type='application/json')
        self.assertEquals(get_canary.status_code, 200)
        self.assertEquals(len(json.loads(get_canary.data).get('results')),
                          results,
                          "Test_Get_Results: Number of results do not match")

    def test_edit_result(self):
        result = self.post_fake_result()
        self.assertEquals(result.status_code, 201)
        self.assertEquals(json.loads(result.data).get('id'), 1)
        edit_result = self.client.put('api/projects/1/canary/1/results/1',
                                      data=json.dumps({'status': 'fail'}),
                                      headers=header)

        self.assertEquals(edit_result.status_code, 200)
        json_data = json.loads(edit_result.data)
        self.assertEquals(json_data.get('status'), 'fail',
                          "EXPECTED {}, GOT {}".format(
                              'fail', json_data.get('status')))
        self.assertEquals(json_data.get('failure_details'), "",
                          "EXPECTED {}, GOT {}".format(
                              "", json_data.get('failure_details')))

    def test_delete_result(self):
        result = self.post_fake_result()
        self.assertEquals(result.status_code, 201)
        self.assertEquals(json.loads(result.data).get('id'), 1)
        wrong_delete = self.client.delete('api/projects/1/canary/2/results/1')
        self.assertEquals(wrong_delete.status_code, 404)
        self.assertEquals(json.loads(wrong_delete.data).get('message'),
                          "result not found")
        delete_result = self.client.delete('api/projects/1/canary/1/results/1')
        self.assertEquals(delete_result.status_code, 204)
