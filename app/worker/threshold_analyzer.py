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
from ..worker.base_analyzer import BaseAnalyzer
from ..worker.clients.api_client import APIClient


class ThresholdAnalyzer(BaseAnalyzer):

    def __init__(self):
        self.api_client = APIClient(base_url="http://localhost:5000")

    def analyze_results(self, criteria, results):
        # return True if green, false if red
        pass

    def process_canary(self, canary_id):
        print canary_id
        # Get canary (to get criteria)
        # Get all results of the canary (future -- get only sample size worth)
        # Call analyze_results: compare results to criteria
        # Based on analysis, update canary health if new health is not the same as old health
        pass
