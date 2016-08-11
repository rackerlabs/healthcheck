from healthcheck.worker.threshold_analyzer import ThresholdAnalyzer


class SampleSizeAnalyzer(ThresholdAnalyzer):
    def __init__(self):
        ThresholdAnalyzer.__init__(self)

    def process_canary(self, canary_id, project_id):
        current_health, criteria = self.get_canary_param(canary_id=canary_id,
                                                         project_id=project_id)
        sample_size = criteria.get('result_sample_size')
        threshold = criteria.get('threshold')
        canary_results = self.api_client.get_results(canary_id=canary_id,
                                                     project_id=project_id,
                                                     sample_size=sample_size)
        green_health = self.analyze_results(threshold=threshold,
                                            results=canary_results)
        if not green_health and current_health == "GREEN":
            update = self.api_client.update_canary(project_id=project_id,
                                                   canary_id=canary_id,
                                                   health="RED")
            assert update.status_code == 200

        elif green_health and current_health == "RED":
            update = self.api_client.update_canary(project_id=project_id,
                                                   canary_id=canary_id,
                                                   health="GREEN")
            assert update.status_code == 200
