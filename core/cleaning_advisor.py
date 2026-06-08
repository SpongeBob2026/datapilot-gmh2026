import pandas as pd


def generate_cleaning_suggestions(df, overview, column_quality, anomaly_summary, fields):
    """
    根据数据概况、字段质量、异常值检测和字段类型生成数据清洗建议。
    """
    suggestions = []

    # 1. 重复行建议
    duplicate_rows = overview.get("重复行数", 0)

    if duplicate_rows > 0:
        suggestions.append({
            "问题类型": "重复数据",
            "涉及字段": "整行数据",
            "问题描述": f"当前数据中存在 {duplicate_rows} 条重复行。",
            "建议处理方式": "建议先核查重复行是否为真实重复记录。如果确认为重复，可删除重复行。",
            "优先级": "高"
        })

    # 2. 缺失值建议
    if not column_quality.empty:
        missing_cols = column_quality[column_quality["缺失值数量"] > 0]

        for _, row in missing_cols.iterrows():
            col = row["字段名"]
            missing_count = row["缺失值数量"]
            missing_rate = row["缺失值比例"]

            if missing_rate >= 0.5:
                priority = "高"
                method = "缺失比例较高，建议核查该字段是否仍有分析价值；必要时可删除该字段或重新采集数据。"
            elif missing_rate >= 0.2:
                priority = "中"
                method = "缺失比例中等，建议结合业务含义选择填补、删除或单独标记缺失。"
            else:
                priority = "低"
                method = "缺失比例较低，可考虑删除缺失行，或使用均值、中位数、众数等方法填补。"

            suggestions.append({
                "问题类型": "缺失值",
                "涉及字段": col,
                "问题描述": f"{col} 字段存在 {missing_count} 个缺失值，缺失比例为 {missing_rate}。",
                "建议处理方式": method,
                "优先级": priority
            })

    # 3. 异常值建议
    if anomaly_summary is not None and not anomaly_summary.empty:
        anomaly_cols = anomaly_summary[anomaly_summary["异常值数量"] > 0]

        for _, row in anomaly_cols.iterrows():
            col = row["字段名"]
            anomaly_count = row["异常值数量"]
            anomaly_rate = row["异常值比例"]
            min_value = row["最小值"]
            max_value = row["最大值"]

            suggestions.append({
                "问题类型": "异常值",
                "涉及字段": col,
                "问题描述": f"{col} 字段检测到 {anomaly_count} 个异常值，异常比例为 {anomaly_rate}，取值范围为 {min_value} 到 {max_value}。",
                "建议处理方式": "建议核查异常值是否为录入错误、极端业务情况或特殊活动数据。不要直接删除，应先结合业务背景判断。",
                "优先级": "高"
            })

    # 4. 日期字段建议
    date_cols = fields.get("date_cols", [])

    for col in date_cols:
        suggestions.append({
            "问题类型": "日期格式",
            "涉及字段": col,
            "问题描述": f"{col} 被识别为日期字段。",
            "建议处理方式": "建议检查日期格式是否统一，后续可按日、周、月进行趋势分析。",
            "优先级": "中"
        })

    # 5. 分类字段建议
    categorical_cols = fields.get("categorical_cols", [])

    for col in categorical_cols:
        unique_count = df[col].nunique(dropna=True)

        suggestions.append({
            "问题类型": "分类字段一致性",
            "涉及字段": col,
            "问题描述": f"{col} 被识别为分类字段，共有 {unique_count} 个不同取值。",
            "建议处理方式": "建议检查是否存在同义不同写、空格、大小写不一致等问题，例如“杭州”和“杭州市”是否需要统一。",
            "优先级": "中"
        })

    # 6. 如果没有明显问题
    if not suggestions:
        suggestions.append({
            "问题类型": "暂无明显清洗问题",
            "涉及字段": "整体数据",
            "问题描述": "当前数据中暂未发现明显重复、缺失或异常问题。",
            "建议处理方式": "可以直接进入统计分析、趋势分析或分组对比分析。",
            "优先级": "低"
        })

    return pd.DataFrame(suggestions)