import numpy as np

def sanitize_json(data):
    if isinstance(data, dict):
        return {k: sanitize_json(v) for k, v in data.items()}

    elif isinstance(data, list):
        return [sanitize_json(v) for v in data]

    elif isinstance(data, float):
        if np.isnan(data) or np.isinf(data):
            return None

    return data