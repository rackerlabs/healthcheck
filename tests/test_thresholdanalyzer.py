import unittest
from healthcheck import create_app, db
from healthcheck.worker.threshold_analyzer import ThresholdAnalyzer
from mock import Mock


data = {'name': 'test canary',
        'description': 'A test canary',
        'meta_data': {'region': 'Hong Kong', 'data2': 'tweete'},
        'criteria': {'threshold': 90, 'expected_run_frequency': '5hrs',
                     'result_sample_size': 10},
        'health': 'GREEN'
        }

expected_data = {'name': 'test canary',
                 'description': 'A test canary',
                 'meta_data': {'region': 'Hong Kong', 'data2': 'tweete'},
                 'status': 'ACTIVE',
                 'health': 'GREEN',
                 'criteria': {'threshold': 90,
                              'expected_run_frequency': '5hrs',
                              'result_sample_size': 10},
                 'id': 1
                 }


class TresholdAnalyzTest(unittest.TestCase):
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

    def test_analyze_results(self):
        analyzer = ThresholdAnalyzer()
        threshold = 70
        red_result = [{"status": "pass", "failure_detils": ""},
                      {"status": "fail", "failure_details": ""},
                      {"status": "fail", "failure_details": ""}]
        result = analyzer.analyze_results(threshold=threshold,
                                          results=red_result)
        self.assertEquals(result, False, "Test_Analyze_Results: Expected {}, "
                                         "got {}".format(False, result))

        green_result = [{"status": "pass", "failure_detils": ""},
                        {"status": "pass", "failure_details": ""},
                        {"status": "pass", "failure_details": ""}]
        result = analyzer.analyze_results(threshold=threshold,
                                          results=green_result)
        self.assertEquals(result, True, "Test_Analyze_Results: Expected {}, "
                                        "got {}".format(True, result))

    def test_get_canary_params(self):
        analyzer = ThresholdAnalyzer()
        analyzer.api_client = Mock()
        analyzer.api_client.get_canary = Mock(name='get_canary',
                                              return_value=expected_data)

        health, criteria = analyzer.get_canary_params(canary_id=1,
                                                      project_id=1)

        self.assertEquals(health, expected_data.get('health'),
                          "Test_Get_Canary_Health: Expected {}"
                          ", got {}".format("GREEN", health))

        self.assertEquals(criteria, expected_data.get('criteria'),
                          "Test_Get_Canary_Criteria: Expected {}"
                          ", got {}".format(data.get('criteria'), criteria))
        analyzer.api_client.get_canary.assert_called_with(project_id=1,
                                                          canary_id=1)
