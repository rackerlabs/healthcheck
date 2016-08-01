"""
Copyright 2016 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import division
from ..worker.base_analyzer import BaseAnalyzer
from ..worker.clients.api_client import APIClient


class ThresholdAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.api_client = APIClient(base_url="http://localhost:5000")

    def analyze_results(self, threshold, results):
        # return True if health needs to be green, false if not
        passes = 0
        fails = 0
        for result in results:
            if result.get('status') == 'pass':
                passes += 1
            else:
                fails += 1
        assert len(results) == (passes + fails)
        pass_percent = passes / len(results) * 100
        if pass_percent < threshold:
            return False
        else:
            return True


    def process_canary(self, canary_id, project_id):
        canary = self.api_client.get_canary(project_id, canary_id)
        current_health = canary.get('health')
        canary_criteria = canary.get('criteria')
        sample_size = canary_criteria.get('result_sample_size')
        canary_results = self.api_client.get_results(project_id=project_id, canary_id=canary_id,
                                                     sample_size=sample_size, interval= None)
        result_list = canary_results.get('results')
        threshold = canary_criteria.get('threshold')
        green_health = self.analyze_results(threshold=threshold, results=result_list)
        if not green_health and current_health == "GREEN":
            # change health to red if not already red
            update = self.api_client.update_canary(project_id=project_id, canary_id=canary_id, health="RED")
            assert update.status_code == 200
        elif green_health and current_health == "RED":
            # change health to green
            update = self.api_client.update_canary(project_id=project_id, canary_id=canary_id, health="GREEN")
            assert update.status_code == 200


