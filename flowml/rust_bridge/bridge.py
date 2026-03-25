import rust_core


# ---------------- CSV ---------------- #

def fast_count_rows(path: str):
    return rust_core.count_rows(path)


def fast_get_headers(path: str):
    return rust_core.get_headers(path)


# ---------------- Cleaning ---------------- #

def fast_drop_nulls(input_path: str):
    output_path = input_path.replace(".csv", "_clean.csv")
    kept = rust_core.drop_nulls(input_path, output_path)
    return output_path, kept


def fast_fill_nulls(input_path: str, value: str = "0"):
    output_path = input_path.replace(".csv", "_filled.csv")
    rust_core.fill_nulls(input_path, output_path, value)
    return output_path


# ---------------- Metrics ---------------- #

def fast_basic_stats(path: str):
    rows, cols = rust_core.basic_stats(path)
    return {
        "rows": rows,
        "columns": cols
    }

def fast_drop_nulls_safe(path: str):
    output_path, kept = fast_drop_nulls(path)

    if kept == 0:
        raise ValueError("All rows removed — unsafe operation")

    return output_path, kept