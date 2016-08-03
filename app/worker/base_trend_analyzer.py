from abc import ABCMeta, abstractmethod


class BaseTrendAnalyzer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_trend(self, project_id, canary_id, interval, resolution, threshold):
        pass
