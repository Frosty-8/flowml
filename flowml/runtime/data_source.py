from .data_loader import load_csv, load_excel, load_from_db


def load_data(source_type: str, config: dict):
    if source_type == "csv":
        return load_csv(config["path"])

    elif source_type == "excel":
        return load_excel(config["path"], config.get("sheet", 0))

    elif source_type == "db":
        return load_from_db(config["connection"], config["query"])

    else:
        raise ValueError("Unsupported data source")