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
from healthcheck.config import get_config
from healthcheck.worker.base_analyzer import BaseAnalyzer
from healthcheck.worker.clients.api_client import APIClient


class ThresholdAnalyzer(BaseAnalyzer):
    def __init__(self):
        config = get_config()
        self.api_client = APIClient(base_url=config.API_URL)

    def analyze_results(self, threshold, results, low_threshold):
        passes = 0
        fails = 0
        for result in results:
            if result.get('status') == 'pass':
                passes += 1
            else:
                fails += 1
        assert len(results) == (passes + fails)
        pass_percent = passes / len(results) * 100
        if pass_percent > float(threshold):
            return "GREEN"
        elif pass_percent >= float(low_threshold):
            return "YELLOW"
        else:
            return "RED"

    def get_canary_param(self, canary_id, project_id):
        canary = self.api_client.get_canary(project_id, canary_id)
        current_health = canary.get('health')
        criteria = canary.get('criteria')
        return current_health, criteria
