import pandas as pd
from flowml.storage.sqlite import get_dataset
from flowml.rust_bridge.bridge import (
    fast_drop_nulls,
    fast_fill_nulls,
    fast_basic_stats
)
import logging
import tempfile
from concurrent.futures import ThreadPoolExecutor
from flowml.runtime.scheduler import safe_notify
import numpy as np
logger = logging.getLogger(__name__)


class PipelineEngine:

    def run(self, job, job_id, dataset_id: str, steps: list):
        dataset = get_dataset(dataset_id)

        if not dataset:
            raise ValueError("Dataset not found")

        current_path = dataset["path"]
        results = []

        total_steps = len(steps)

        # 🔥 Initial progress
        job.progress = 5
        job.current_step = "starting"
        safe_notify(job_id)

        for i, step in enumerate(steps):
            name = step.get("step")
            params = step.get("params", {})

            # 🔥 Progress update
            job.current_step = name
            job.progress = int((i / total_steps) * 100)

            safe_notify(job_id)

            logger.info(f"[PIPELINE] Running step: {name} ({job.progress}%)")

            # ---------------- FILL NULLS ----------------
            if name == "fill_nulls":
                value = params.get("value", "0")

                output_path = fast_fill_nulls(current_path, value)
                current_path = output_path

                results.append({
                    "step": name,
                    "status": "done",
                    "fill_value": value
                })

            # ---------------- DROP NULLS ----------------
            elif name == "drop_nulls":

                threshold = params.get("threshold")
                columns = params.get("columns")

                df = pd.read_csv(current_path)
                before = len(df)

                if columns:
                    df_clean = df.dropna(subset=columns)

                elif threshold is not None:
                    min_non_null = int((1 - threshold) * df.shape[1])
                    df_clean = df.dropna(thresh=min_non_null)

                else:
                    output_path, kept = fast_drop_nulls(current_path)

                    results.append({
                        "step": name,
                        "rows_before": before,
                        "rows_after": kept,
                        "rows_removed": before - kept,
                        "mode": "rust_all"
                    })

                    current_path = output_path
                    continue

                after = len(df_clean)

                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
                df_clean.to_csv(temp_file.name, index=False)

                current_path = temp_file.name

                results.append({
                    "step": name,
                    "rows_before": before,
                    "rows_after": after,
                    "rows_removed": before - after,
                    "mode": "smart"
                })

            # ---------------- SUMMARY ----------------
            elif name == "summary":
                stats = fast_basic_stats(current_path)

                results.append({
                    "step": name,
                    "stats": stats
                })

            else:
                raise ValueError(f"Unknown step: {name}")

        # 🔥 Final update
        job.progress = 100
        job.current_step = "completed"
        safe_notify(job_id)

        return {
            "final_path": current_path,
            "results": results
        }