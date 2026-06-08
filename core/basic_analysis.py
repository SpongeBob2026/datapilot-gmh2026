import pandas as pd


def get_overview(df):
    """
    数据整体概况。
    """
    total_cells = df.shape[0] * df.shape[1]

    return {
        "行数": len(df),
        "列数": len(df.columns),
        "重复行数": int(df.duplicated().sum()),
        "缺失值总数": int(df.isna().sum().sum()),
        "缺失值比例": round(float(df.isna().sum().sum() / total_cells), 4) if total_cells > 0 else 0,
    }


def get_column_quality(df):
    """
    每一列的数据质量。
    """
    result = []

    for col in df.columns:
        missing_count = int(df[col].isna().sum())
        missing_rate = round(float(missing_count / len(df)), 4) if len(df) > 0 else 0

        result.append({
            "字段名": col,
            "数据类型": str(df[col].dtype),
            "缺失值数量": missing_count,
            "缺失值比例": missing_rate,
            "唯一值数量": int(df[col].nunique(dropna=True)),
        })

    return pd.DataFrame(result)


def get_numeric_summary(df):
    """
    数值列描述统计。
    """
    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        return pd.DataFrame()

    summary = numeric_df.describe().T

    summary = summary.rename(columns={
        "count": "非空数量",
        "mean": "平均值",
        "std": "标准差",
        "min": "最小值",
        "25%": "25%分位数",
        "50%": "中位数",
        "75%": "75%分位数",
        "max": "最大值",
    })

    return summary.round(4)