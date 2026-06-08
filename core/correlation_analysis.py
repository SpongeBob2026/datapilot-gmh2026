import pandas as pd


def get_correlation_matrix(df):
    """
    计算数值字段之间的相关系数矩阵。
    """
    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.shape[1] < 2:
        return pd.DataFrame()

    corr = numeric_df.corr(method="pearson")

    return corr.round(4)


def get_strong_correlations(df, threshold=0.7):
    """
    提取强相关字段对。
    threshold 默认为 0.7。
    """
    corr = get_correlation_matrix(df)

    if corr.empty:
        return pd.DataFrame()

    results = []

    cols = corr.columns.tolist()

    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            col1 = cols[i]
            col2 = cols[j]
            value = corr.loc[col1, col2]

            if pd.notna(value) and abs(value) >= threshold:
                if value > 0:
                    relation = "正相关"
                else:
                    relation = "负相关"

                results.append({
                    "字段1": col1,
                    "字段2": col2,
                    "相关系数": round(float(value), 4),
                    "关系类型": relation,
                    "说明": f"{col1} 与 {col2} 存在较强{relation}关系"
                })

    return pd.DataFrame(results)