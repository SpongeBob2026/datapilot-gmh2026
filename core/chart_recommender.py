import pandas as pd


def recommend_charts(df, fields):
    """
    根据字段类型推荐适合的图表。
    返回推荐图表列表。
    """
    numeric_cols = fields.get("numeric_cols", [])
    categorical_cols = fields.get("categorical_cols", [])
    date_cols = fields.get("date_cols", [])
    text_cols = fields.get("text_cols", [])

    recommendations = []

    # 日期 + 数值：趋势图
    if date_cols and numeric_cols:
        for date_col in date_cols[:2]:
            for numeric_col in numeric_cols[:3]:
                recommendations.append({
                    "推荐图表": "折线图",
                    "适用字段": f"{date_col} + {numeric_col}",
                    "适合分析的问题": f"观察 {numeric_col} 随时间的变化趋势",
                    "推荐理由": "数据中同时存在日期字段和数值字段，适合做时间趋势分析。"
                })

    # 分类 + 数值：柱状图
    if categorical_cols and numeric_cols:
        for cat_col in categorical_cols[:3]:
            for numeric_col in numeric_cols[:3]:
                recommendations.append({
                    "推荐图表": "柱状图",
                    "适用字段": f"{cat_col} + {numeric_col}",
                    "适合分析的问题": f"比较不同 {cat_col} 下的 {numeric_col} 差异",
                    "推荐理由": "数据中同时存在分类字段和数值字段，适合做分组对比分析。"
                })

    # 单个分类字段：频数柱状图
    if categorical_cols:
        for cat_col in categorical_cols[:3]:
            recommendations.append({
                "推荐图表": "频数柱状图",
                "适用字段": cat_col,
                "适合分析的问题": f"查看 {cat_col} 中不同类别的出现次数",
                "推荐理由": "分类字段适合统计各类别频数，用于观察类别分布。"
            })

    # 单个数值字段：直方图
    if numeric_cols:
        for numeric_col in numeric_cols[:3]:
            recommendations.append({
                "推荐图表": "直方图",
                "适用字段": numeric_col,
                "适合分析的问题": f"观察 {numeric_col} 的数值分布情况",
                "推荐理由": "数值字段适合用直方图观察集中区间、离散程度和异常值。"
            })

    # 两个数值字段：散点图
    if len(numeric_cols) >= 2:
        for i in range(min(len(numeric_cols), 3)):
            for j in range(i + 1, min(len(numeric_cols), 3)):
                col1 = numeric_cols[i]
                col2 = numeric_cols[j]
                recommendations.append({
                    "推荐图表": "散点图",
                    "适用字段": f"{col1} + {col2}",
                    "适合分析的问题": f"观察 {col1} 与 {col2} 之间是否存在相关关系",
                    "推荐理由": "两个数值字段适合用散点图观察相关性、聚集形态和异常点。"
                })

    # 文本字段：暂不直接画图
    if text_cols:
        for text_col in text_cols[:2]:
            recommendations.append({
                "推荐图表": "文本分析图",
                "适用字段": text_col,
                "适合分析的问题": f"分析 {text_col} 的关键词、高频词或文本长度分布",
                "推荐理由": "文本字段不适合直接用普通统计图展示，后续可扩展关键词分析和词频统计。"
            })

    return pd.DataFrame(recommendations)