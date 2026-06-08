import pandas as pd


def detect_fields(df):
    """
    自动识别数值列、日期列、分类列、文本列。
    """
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    date_cols = []
    categorical_cols = []
    text_cols = []

    for col in df.columns:
        if col in numeric_cols:
            continue

        series = df[col].dropna()

        if series.empty:
            continue

        # 转成字符串再尝试识别日期，避免 CSV 读取后日期被当作普通文本
        series_str = series.astype(str).str.strip()

        try:
            parsed = pd.to_datetime(series_str, errors="coerce", format="mixed")
        except TypeError:
            parsed = pd.to_datetime(series_str, errors="coerce")

        date_ratio = parsed.notna().mean()

        # 如果 70% 以上都能被解析成日期，就认为是日期字段
        if date_ratio >= 0.7:
            date_cols.append(col)
            continue

        unique_count = series.nunique()
        total_count = len(series)

        # 唯一值较少，通常认为是分类字段
        if unique_count <= 30 or unique_count / total_count <= 0.3:
            categorical_cols.append(col)
        else:
            text_cols.append(col)

    return {
        "numeric_cols": numeric_cols,
        "date_cols": date_cols,
        "categorical_cols": categorical_cols,
        "text_cols": text_cols,
    }