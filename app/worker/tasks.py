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
from celery import Celery
from threshold_analyzer import ThresholdAnalyzer

worker_app = Celery("canary_analyzer", broker="redis://192.168.99.100:6379/0",
                    include=["app.worker.tasks"])

analyzer = ThresholdAnalyzer()


@worker_app.task
def process_canary(canary_id, project_id):
    analyzer.process_canary(project_id=project_id, canary_id=canary_id)
