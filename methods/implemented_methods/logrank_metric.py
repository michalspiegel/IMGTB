from methods.abstract_methods.metric_based_experiment import MetricBasedExperiment
from methods.utils import get_rank

import numpy as np


class LogRankMetric(MetricBasedExperiment):
    def __init__(self, data, config):
        super().__init__(data, self.__class__.__name__, config)
    
    def criterion_fn(self, text: str):
        return np.array([get_rank(text, self.base_model, self.base_tokenizer, self.DEVICE, log=True)])