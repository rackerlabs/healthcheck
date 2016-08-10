from __future__ import division
from datetime import datetime, timedelta
from ..worker.base_trend_analyzer import BaseTrendAnalyzer
from ..worker.clients.api_client import APIClient


class TrendAnalyzer(BaseTrendAnalyzer):
    def __init__(self):
        self.api_client = APIClient(base_url="http://localhost:5000")

    def process_trend(self, resolution, threshold, results_list):
        results_list = sorted(results_list)
        resolution = self.time_conversion(resolution)
        status_list = []
        length = len(results_list)
        analysis_list = []
        time_format = '%Y-%m-%d %H:%M:%S.%f'
        start_time = datetime.strptime(results_list[0].get('created_at'),
                                       format=time_format)
        border = start_time + resolution
        index = 0
        labels = []
        while index < length:
            if index != length - 1:
                created_at = datetime.strptime(results_list[index].
                                               get('created_at'),
                                               format=time_format)
                if created_at <= border:
                    analysis_list.append(results_list[index].
                                         get('status'))
                    index += 1
                else:
                    if analysis_list:
                        labels.append("{}".format(border - resolution))
                        result = self.trend_analyzer(threshold, analysis_list)
                        status_list.append(result)
                        analysis_list = []
                    border = border + resolution
            else:
                created_at = datetime.strptime(results_list[index].
                                               get('created_at'),
                                               format=time_format)
                if created_at <= border:
                    labels.append("{}".format(border - resolution))
                    analysis_list.append(results_list[index].get('status'))
                    result = self.trend_analyzer(threshold, analysis_list)
                    status_list.append(result)
                else:
                    labels.append("{}".format(border - resolution))
                    result = self.trend_analyzer(threshold, analysis_list)
                    status_list.append(result)
                    analysis_list = []
                    border = border + resolution
                    while True:
                        if created_at <= border:
                            labels.append("{}".format(border - resolution))
                            analysis_list.append(
                                results_list[index].get('status'))
                            result = self.trend_analyzer(
                                threshold, analysis_list)
                            status_list.append(result)
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
