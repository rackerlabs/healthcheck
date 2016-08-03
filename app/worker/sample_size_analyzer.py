from ..worker.threshold_analyzer import ThresholdAnalyzer


class SampleSizeAnalyzer(ThresholdAnalyzer):
    def __init__(self):
        ThresholdAnalyzer.__init__(self)

    def process_canary(self, canary_id, project_id):
        current_health, criteria = self.get_canary_params(canary_id=canary_id, project_id=project_id)
        sample_size = criteria.get('result_sample_size')
        threshold = criteria.get('threshold')
        canary_results = self.get_results(canary_id=canary_id, project_id=project_id, sample_size=sample_size,
                                          interval=None)
        green_health = self.analyze_results(threshold=threshold, results=canary_results)
        self.change_health(current_health=current_health, green_health=green_health, project_id=project_id,
                           canary_id=canary_id)
