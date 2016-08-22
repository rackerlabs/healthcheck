import unittest
from healthcheck import create_app, db
from healthcheck.worker.trend_analyzer import TrendAnalyzer
from datetime import datetime

results = [{u'status': u'pass', u'created_at': u'2016-08-08 07:11:34.878709',
            u'failure_details': u'', u'id': 1},
           {u'status': u'pass', u'created_at': u'2016-08-09 07:33:45.878709',
            u'failure_details': u'', u'id': 2},
           {u'status': u'fail', u'created_at': u'2016-08-10 02:11:56.878709',
            u'failure_details': u'', u'id': 3},
           {u'status': u'pass', u'created_at': u'2016-08-08 05:12:34.878709',
            u'failure_details': u'', u'id': 4},
           {u'status': u'pass', u'created_at': u'2016-08-09 07:12:12.878709',
            u'failure_details': u'', u'id': 5},
           {u'status': u'pass', u'created_at': u'2016-08-10 02:15:45.878709',
            u'failure_details': u'', u'id': 6},
           {u'status': u'pass', u'created_at': u'2016-08-08 01:31:44.878709',
            u'failure_details': u'', u'id': 7},
           {u'status': u'pass', u'created_at': u'2016-08-08 07:03:36.878709',
            u'failure_details': u'', u'id': 8},
           {u'status': u'pass', u'created_at': u'2016-08-10 10:11:34.878709',
            u'failure_details': u'', u'id': 9},
           {u'status': u'pass', u'created_at': u'2016-08-08 23:11:34.878709',
            u'failure_details': u'', u'id': 10},
           {u'status': u'pass', u'created_at': u'2016-08-09 12:23:34.878709',
            u'failure_details': u'', u'id': 11},
           {u'status': u'pass', u'created_at': u'2016-08-10 13:15:44.878709',
            u'failure_details': u'', u'id': 12},
           {u'status': u'pass', u'created_at': u'2016-08-08 07:35:45.878709',
            u'failure_details': u'', u'id': 13},
           {u'status': u'pass', u'created_at': u'2016-08-10 09:11:34.878709',
            u'failure_details': u'', u'id': 14},
           {u'status': u'pass', u'created_at': u'2016-08-10 06:15:45.878709',
            u'failure_details': u'', u'id': 15},
           {u'status': u'pass', u'created_at': u'2016-08-08 03:10:56.878709',
            u'failure_details': u'', u'id': 16},
           {u'status': u'pass', u'created_at': u'2016-08-08 22:11:32.878709',
            u'failure_details': u'', u'id': 17},
           {u'status': u'fail', u'created_at': u'2016-08-10 15:10:45.878709',
            u'failure_details': u'', u'id': 18},
           ]


class TrendAnalyzerTest(unittest.TestCase):
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

    def test_trend_analyzer(self):
        trend = TrendAnalyzer()
        resolution = "1 days"
        threshold = 80
        results_list = results
        interval = "3 days"
        start_time = datetime.strptime("2016-08-10 14:00:44.878709", "%Y-%m-%d %H:%M:%S.%f")
        expected_status_list = ['green', 'green', 'red']
        expected_labels = ['2016-08-08 01:31:44.878709',
                           '2016-08-09 01:31:44.878709',
                           '2016-08-10 01:31:44.878709']
        status_list, labels = trend.process_trend(resolution=resolution,
                                                  threshold=threshold,
                                                  results_list=results_list,
                                                  interval=interval,
                                                  start_time=start_time)
        self.assertEquals(status_list, expected_status_list,
                          "Status List result does not match")

        self.assertEquals(labels, expected_labels,
                          "Labels List result does not match")
