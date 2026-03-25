from collections import defaultdict


class MetricsEngine:
    def __init__(self):
        self.request_count = 0
        self.endpoint_counts = defaultdict(int)
        self.errors = 0
        self.latencies = []

        self.data_stats = []
        self.cleaning_stats = []

    # ---------------------------
    # Request Metrics
    # ---------------------------
    def log_request(self, endpoint: str, latency: float):
        self.request_count += 1
        self.endpoint_counts[endpoint] += 1
        self.latencies.append(latency)

    def log_error(self):
        self.errors += 1

    def get_request_metrics(self):
        avg_latency = (
            sum(self.latencies) / len(self.latencies)
            if self.latencies else 0
        )

        return {
            "total_requests": self.request_count,
            "errors": self.errors,
            "avg_latency": round(avg_latency, 4),
            "endpoints": dict(self.endpoint_counts)
        }

    # ---------------------------
    # Data Metrics
    # ---------------------------
    def log_data_stats(self, stats: dict):
        self.data_stats.append(stats)

    def get_data_metrics(self):
        return self.data_stats[-5:]

    # ---------------------------
    # Cleaning Metrics
    # ---------------------------
    def log_cleaning(self, data):
        self.cleaning_stats.append({
            "operation": data.get("operation"),
            "rows_before": data.get("rows_before"),
            "rows_after": data.get("rows_after"),
            "rows_removed": data.get("rows_removed"),
        })

    def get_cleaning_metrics(self):
        return self.cleaning_stats[-5:]