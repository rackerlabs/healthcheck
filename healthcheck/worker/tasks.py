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

from healthcheck.config import get_config
from sample_size_analyzer import SampleSizeAnalyzer
from trend_analyzer import TrendAnalyzer

config = get_config()
worker_app = Celery("canary_analyzer", broker=config.CELERY_BROKER_URL,
                    backend=config.CELERY_RESULT_BACKEND,
                    include=["healthcheck.worker.tasks"])

analyzer = SampleSizeAnalyzer()
trend = TrendAnalyzer()


@worker_app.task
def process_canary(canary_id, project_id):
    analyzer.process_canary(project_id=project_id, canary_id=canary_id)


@worker_app.task
def process_trend(resolution, threshold, results_list):
    return trend.process_trend(resolution=resolution,
                               threshold=threshold, results_list=results_list)
