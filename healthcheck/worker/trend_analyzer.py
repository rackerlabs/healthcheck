from __future__ import division
from datetime import datetime, timedelta
from healthcheck.config import get_config
from healthcheck.worker.base_trend_analyzer import BaseTrendAnalyzer
from healthcheck.worker.clients.api_client import APIClient



results = [{u'status': u'pass', u'created_at': u'2016-08-19 07:11:34.878709',
            u'failure_details': u'', u'id': 1},
           {u'status': u'pass', u'created_at': u'2016-08-16 07:33:45.878709',
            u'failure_details': u'', u'id': 2},
           {u'status': u'fail', u'created_at': u'2016-08-19 02:11:56.878709',
            u'failure_details': u'', u'id': 3},
           {u'status': u'pass', u'created_at': u'2016-08-19 05:12:34.878709',
            u'failure_details': u'', u'id': 4},
           {u'status': u'pass', u'created_at': u'2016-08-16 07:12:12.878709',
            u'failure_details': u'', u'id': 5},
           {u'status': u'pass', u'created_at': u'2016-08-17 02:15:45.878709',
            u'failure_details': u'', u'id': 6},
           {u'status': u'pass', u'created_at': u'2016-08-16 01:31:44.878709',
            u'failure_details': u'', u'id': 7},
           {u'status': u'pass', u'created_at': u'2016-08-15 07:03:36.878709',
            u'failure_details': u'', u'id': 8},
           {u'status': u'pass', u'created_at': u'2016-08-15 10:11:34.878709',
            u'failure_details': u'', u'id': 9},
           {u'status': u'pass', u'created_at': u'2016-08-16 23:11:34.878709',
            u'failure_details': u'', u'id': 10},
           ]

class TrendAnalyzer(BaseTrendAnalyzer):
    def __init__(self):
        config = get_config()
        self.api_client = APIClient(base_url=config.API_URL)

    def process_trend(self, resolution, threshold, interval, start_time):
        results_list = sorted(results)
        for res in results_list:
            print res
            print '\n'

        resolution = self.time_conversion(resolution)
        status_list = []
        length = len(results_list)
        analysis_list = []
        time_format = '%Y-%m-%d %H:%M:%S.%f'
        interval = self.time_conversion(interval)
        border = start_time - interval + resolution
        index = 0
        labels = []
        my_list = []
        while index < length:
            created_at = datetime.strptime(results_list[index].
                                           get('created_at'),
                                           time_format)
            print "BORDER AT INDEX {} IS {}".format(index, border)
            if created_at <= border:
                analysis_list.append(results_list[index].get('status'))
                my_list.append(self.Example(results_list[index].get('status'), results_list[index].get('id')))
            else:
                labels.append("{}".format(border - resolution))
                result = self.trend_analyzer(threshold, analysis_list)
                status_list.append(result)
                print "INSIDE THE ELSE", my_list
                analysis_list = []
                my_list = []
                analysis_list.append(results_list[index].get('status'))
                my_list.append(self.Example(results_list[index].get('status'), results_list[index].get('id')))
                border = border + resolution

            if index == length - 1:
                labels.append("{}".format(border - resolution))
                result = self.trend_analyzer(threshold, analysis_list)
                status_list.append(result)
                print "FINALLY", my_list

            index += 1

        print "STATUS LIST IS", status_list
        print "LABELS IS ", labels
        return status_list, labels

    def trend_analyzer(self, threshold, results_list):
        if results_list:
            passes = 0
            fails = 0
            for result in results_list:
                if result == 'pass':
                    passes += 1
                else:
                    fails += 1
            assert len(results_list) == (passes + fails)
            pass_percent = passes / len(results_list) * 100
            if pass_percent > float(threshold):
                return "green"
            else:
                return "red"

    def time_conversion(self, time_value):
        value = time_value.split()
        if value[1] == "days":
            return timedelta(days=int(value[0]))
        elif value[1] == "hours":
            return timedelta(hours=int(value[0]))


    class Example():
        def __init__(self, status, id):
            self.status = status
            self.id = id

        def __repr__(self):
            return "[id = %d, status = %s]" % (self.id, self.status)