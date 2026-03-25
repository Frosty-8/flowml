from .metrics_engine import MetricsEngine


class Registry:
    def __init__(self):
        self.models = {}
        self.metrics_engine = MetricsEngine()


registry = Registry()
