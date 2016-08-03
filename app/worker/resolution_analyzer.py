from ..worker.threshold_analyzer import ThresholdAnalyzer


class ResolutionAnalyzer(ThresholdAnalyzer):
    def __init__(self):
        ThresholdAnalyzer.__init__(self)

    def process_canary(self, project_id, canary_id):  # time should be in hours, or day
        current_health, criteria = self.get_canary_params(canary_id=canary_id, project_id=project_id)
        resolution = criteria.get('resolution')
        threshold = criteria.get('threshold')
        canary_results = self.get_results(canary_id=canary_id, project_id=project_id, sample_size=None,
                                          interval=resolution)
        green_health = self.analyze_results(threshold=threshold, results=canary_results)
        self.change_health(current_health=current_health, green_health=green_health, project_id=project_id,
                           canary_id=canary_id)
