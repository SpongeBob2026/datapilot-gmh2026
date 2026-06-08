import pandas as pd


def detect_numeric_anomalies(df):
    """
    使用 IQR 四分位距方法检测数值列异常值。
    返回异常值汇总表。
    """
    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        return pd.DataFrame()

    results = []

    for col in numeric_df.columns:
        series = numeric_df[col].dropna()

        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        anomaly_count = int(((series < lower_bound) | (series > upper_bound)).sum())
        anomaly_rate = round(anomaly_count / len(series), 4)

        results.append({
            "字段名": col,
            "下界": round(lower_bound, 4),
            "上界": round(upper_bound, 4),
            "异常值数量": anomaly_count,
            "异常值比例": anomaly_rate,
            "最小值": round(series.min(), 4),
            "最大值": round(series.max(), 4),
        })

    return pd.DataFrame(results)