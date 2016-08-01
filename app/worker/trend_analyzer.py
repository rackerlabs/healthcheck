from __future__ import division
from ..worker.base_trend_analyzer import BaseTrendAnalyzer
from ..worker.clients.api_client import APIClient
from datetime import datetime, timedelta


class TrendAnalyzer(BaseTrendAnalyzer):
    def __init__(self):
        self.api_client = APIClient(base_url="http://localhost:5000")

    def process_trend(self, project_id, canary_id, interval, resolution, threshold, results):
        # results = self.api_client.get_results(project_id=project_id, canary_id=canary_id, interval=interval, sample_size=None)
        # results_list = results.get('results')
        resolution = self.time_conversion(resolution)
        status_list = []
        length = len(results)
        analysis_list = []
        example_list = []
        start_time = datetime.strptime(results[0].get('created_at'), '%a, %d %b %Y %H:%M:%S %Z')
        border = start_time + resolution
        index = 0
        while index < length:
            print results[index].get("id"), datetime.strptime(results[index].get('created_at'),
                                                          '%a, %d %b %Y %H:%M:%S %Z')
            if index != length - 1:
                if datetime.strptime(results[index].get('created_at'), '%a, %d %b %Y %H:%M:%S %Z') <= border:
                    analysis_list.append(results[index].get('status'))
                    example_list.append(self.Example(results[index].get('status'), results[index].get('id')))
                    index += 1
                else:
                    print example_list
                    if analysis_list:
                        status_list.append(self.trend_analyzer(threshold, analysis_list))
                        analysis_list = []
                        example_list = []
                    border = border + resolution
            else:
                analysis_list.append(results[index].get('status'))
                status_list.append(self.trend_analyzer(threshold, analysis_list))
                break
        print "STATUS LIST IS"
        print status_list


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


    class Example():
        def __init__(self, status, id):
            self.status = status
            self.id = id

        def __repr__(self):
            return "[id = %d, status = %s]" % (self.id, self.status)


    def time_conversion(self, time_value):
        value = time_value.split()
        if value[1] == "days":
            return timedelta(days=int(value[0]))
        elif value[1] == "hours":
            return timedelta(hours=int(value[0]))






