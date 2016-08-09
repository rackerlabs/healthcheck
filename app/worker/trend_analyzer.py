from __future__ import division
from datetime import datetime, timedelta
from ..worker.base_trend_analyzer import BaseTrendAnalyzer
from ..worker.clients.api_client import APIClient


class TrendAnalyzer(BaseTrendAnalyzer):
    def __init__(self):
        self.api_client = APIClient(base_url="http://localhost:5000")

    def process_trend(self, resolution, threshold, results_list):
        results_list = sorted(results_list)

        for result in results_list:
            print result
            print '\n'

        resolution = self.time_conversion(resolution)
        status_list = []
        length = len(results_list)
        analysis_list = []
        start_time = datetime.strptime(results_list[0].get('created_at'), '%Y-%m-%d %H:%M:%S.%f')
        border = start_time + resolution
        index = 0
        labels = []
        example_list = []
        while index < length:
            if index != length - 1:
                created_at = datetime.strptime(results_list[index].get('created_at'), '%Y-%m-%d %H:%M:%S.%f')
                if created_at <= border:
                    example_list.append(Example(results_list[index].get('status'), results_list[index].get('id')))
                    analysis_list.append(results_list[index].get('status'))
                    index += 1
                else:
                    if analysis_list:
                        labels.append("{}".format(border - resolution))
                        print "EXAMPLE ", example_list
                        status_list.append(self.trend_analyzer(threshold, analysis_list))
                        analysis_list = []
                        example_list = []
                    border = border + resolution
            else:
                created_at = datetime.strptime(results_list[index].get('created_at'), '%Y-%m-%d %H:%M:%S.%f')
                if created_at <= border:
                    labels.append("{}".format(border - resolution))
                    example_list.append(Example(results_list[index].get('status'), results_list[index].get('id')))
                    analysis_list.append(results_list[index].get('status'))
                    print "EXAMPLE LIST" , example_list
                    status_list.append(self.trend_analyzer(threshold, analysis_list))
                else:
                    labels.append("{}".format(border - resolution))
                    print  "EXAMPLE LIST" , example_list
                    status_list.append(self.trend_analyzer(threshold, analysis_list))
                    analysis_list = []
                    example_list = []
                    border = border + resolution
                    while True:
                        if created_at <= border:
                            labels.append("{}".format(border - resolution))
                            analysis_list.append(results_list[index].get('status'))
                            example_list.append(Example(results_list[index].get('status'), results_list[index].get('id')))
                            print "EXAMPLE LIST",  example_list
                            status_list.append(self.trend_analyzer(threshold, analysis_list))
                            break
                        else:
                            border = border + resolution
                index += 1
        print "STATUS LIST IS", status_list
        print "LABELS IS ", labels
        return status_list, labels

    def trend_analyzer(self, threshold, results_list):
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

