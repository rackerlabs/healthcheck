from __future__ import division
from datetime import datetime, timedelta
from healthcheck.config import get_config
from healthcheck.worker.base_trend_analyzer import BaseTrendAnalyzer
from healthcheck.worker.clients.api_client import APIClient


class TrendAnalyzer(BaseTrendAnalyzer):
    def __init__(self):
        config = get_config()
        self.api_client = APIClient(base_url=config.API_URL)

    def process_trend(self, resolution, interval, start_time,
                      results_list):
        results_list = sorted(results_list)
        resolution = self.time_conversion(resolution)
        status_list = []
        length = len(results_list)
        analysis_list = []
        time_format = '%Y-%m-%d %H:%M:%S.%f'
        interval = self.time_conversion(interval)
        border = start_time - interval + resolution
        index = 0
        labels = []
        while index < length:
            created_at = datetime.strptime(results_list[index].
                                           get('created_at'),
                                           time_format)
            if created_at <= border:
                analysis_list.append(results_list[index].get('status'))
            else:
                labels.append("{}".format(border - resolution))
                result = self.trend_analyzer(analysis_list)
                status_list.append(result)
                analysis_list = []
                analysis_list.append(results_list[index].get('status'))
                border = border + resolution

            if index == length - 1:
                labels.append("{}".format(border - resolution))
                result = self.trend_analyzer(analysis_list)
                status_list.append(result)

            index += 1

        print "STATUS LIST IS", status_list
        print "LABELS IS ", labels
        return status_list, labels

    def trend_analyzer(self,results_list):
        passes = 0
        fails = 0
        for result in results_list:
            if result == 'pass':
                passes += 1
            else:
                fails += 1
        assert len(results_list) == (passes + fails)
        pass_percent = passes / len(results_list) * 100
        return pass_percent

    def time_conversion(self, time_value):
        value = time_value.split()
        if value[1] == "days":
            return timedelta(days=int(value[0]))
        elif value[1] == "hours":
            return timedelta(hours=int(value[0]))
