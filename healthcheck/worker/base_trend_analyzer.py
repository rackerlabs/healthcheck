from abc import ABCMeta, abstractmethod


class BaseTrendAnalyzer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_trend(self, resolution, interval, start_time,
                      results_list):
        pass
