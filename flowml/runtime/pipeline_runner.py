import pandas as pd
from flowml.storage.sqlite import get_dataset


def run_pipeline(dataset_id: str, steps: list):
    dataset = get_dataset(dataset_id)

    if not dataset:
        raise ValueError("Dataset not found")

    path = dataset["path"]
    df = pd.read_csv(path)

    results = []

    for step in steps:
        name = step["step"]

        if name == "fill_nulls":
            value = step.get("params", {}).get("value", "0")
            df = df.fillna(value)

            results.append(
                {"step": "fill_nulls", "status": "done", "fill_value": value}
            )

        elif name == "drop_nulls":
            before = len(df)
            df = df.dropna()
            after = len(df)

            results.append(
                {
                    "step": "drop_nulls",
                    "rows_before": before,
                    "rows_after": after,
                    "rows_removed": before - after,
                }
            )

        elif name == "summary":
            results.append(
                {
                    "step": "summary",
                    "stats": {"rows": df.shape[0], "columns": df.shape[1]},
                }
            )

    output_path = path.replace(".csv", "_pipeline.csv")
    df.to_csv(output_path, index=False)

    return {"final_path": output_path, "results": results}
