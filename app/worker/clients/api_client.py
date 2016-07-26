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
from data_client import DataClient
import requests, json


class APIClient(DataClient):
    def __init__(self, base_url):
        self.base_url = base_url

    def get_canary(self, project_id, canary_id):
        canary_url = "{base_url}/api/projects/{project_id}/canary/{canary_id}".format(
            base_url=self.base_url, project_id=project_id, canary_id=canary_id)
        canary = requests.get(canary_url)
        return canary.json()

    def update_canary(self, project_id, canary_id, health):
        # try to use url_for (api.get_canary)....
        canary_url = "{base_url}/api/projects/{project_id}/canary/{canary_id}".format(
            base_url=self.base_url, project_id=project_id, canary_id=canary_id)
        update = requests.put(canary_url, data=json.dumps({'health': health}),
                              headers={'content-type': 'application/json'})
        return update

    def get_results(self, project_id, canary_id, sample_size):
        canary_url = "{base_url}/api/projects/{project_id}/canary/{canary_id}/results?limit={sample_size}".format(
            base_url=self.base_url, project_id=project_id, canary_id=canary_id, sample_size=sample_size)
        canary_results = requests.get(canary_url)
        return canary_results.json()
