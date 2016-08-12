import unittest
from app import create_app, db
from app.worker.sample_size_analyzer import SampleSizeAnalyzer
from mock import Mock

canary_data = {'name': 'test canary',
               'description': 'A test canary',
               'meta_data': {'region': 'Hong Kong', 'data2': 'tweete'},
               'status': 'ACTIVE',
               'health': 'GREEN',
               'criteria': {'threshold': 90,
                            'expected_run_frequency': '5hrs',
                            'result_sample_size': 3},
               'id': 1
               }

canary_red_data = {'name': 'test canary',
                   'description': 'A test canary',
                   'meta_data': {'region': 'Hong Kong', 'data2': 'tweete'},
                   'status': 'ACTIVE',
                   'health': 'RED',
                   'criteria': {'threshold': 90,
                                'expected_run_frequency': '5hrs',
                                'result_sample_size': 3},
                   'id': 1
                   }

canary_red_results = [{"status": "pass", "failure_detils": ""},
                      {"status": "fail", "failure_details": ""},
                      {"status": "pass", "failure_details": ""}]

canary_green_results = [{"status": "pass", "failure_detils": ""},
                        {"status": "pass", "failure_details": ""},
                        {"status": "pass", "failure_details": ""}]


class SampleSizeTest(unittest.TestCase):
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

    def mocked_requests_get(self):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(canary_red_data, 200)

    def test_red_processcanary(self):
        sample_size_analyzer = SampleSizeAnalyzer()
        sample_size_analyzer.api_client = Mock()
        sample_size_analyzer.api_client.update_canary = Mock(
            name='update_canary', return_value=self.mocked_requests_get())
        sample_size_analyzer.get_canary_params = Mock(
            name='get_canary_params', return_value=[canary_data.get('health'),
                                                    canary_data.get(
                                                        'criteria')])
        sample_size_analyzer.api_client.get_results = Mock(
            name='get_results', return_value=canary_red_results)

        sample_size_analyzer.process_canary(canary_id=1, project_id=1)
        sample_size_analyzer.api_client.update_canary.assert_called_with(
            project_id=1, canary_id=1, health="RED")

    def test_green_processcanary(self):
        sample_size_analyzer = SampleSizeAnalyzer()
        sample_size_analyzer.api_client = Mock()
        sample_size_analyzer.api_client.update_canary = Mock(
            name='update_canary', return_value=self.mocked_requests_get())
        sample_size_analyzer.get_canary_params = Mock(
            name='get_canary_params',
            return_value=[canary_red_data.get('health'),
                          canary_data.get('criteria')])
        sample_size_analyzer.api_client.get_results = Mock(
            name='get_results',
            return_value=canary_green_results)

        sample_size_analyzer.process_canary(canary_id=1, project_id=1)
        sample_size_analyzer.api_client.update_canary.assert_called_with(
            project_id=1, canary_id=1, health="GREEN")

    def test_no_processcanary(self):
        sample_size_analyzer = SampleSizeAnalyzer()
        sample_size_analyzer.api_client = Mock()
        sample_size_analyzer.api_client.update_canary = Mock(
            name='update_canary', return_value=self.mocked_requests_get())
        sample_size_analyzer.get_canary_params = Mock(
            name='get_canary_params',
            return_value=[canary_data.get('health'),
                          canary_data.get('criteria')])
        sample_size_analyzer.api_client.get_results = Mock(
            name='get_results',
            return_value=canary_green_results)

        sample_size_analyzer.process_canary(canary_id=1, project_id=1)
        sample_size_analyzer.api_client.update_canary.assert_not_called()
