import os
import tempfile

import pandas as pd

os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "datapilot_matplotlib"))

import matplotlib.pyplot as plt


def generate_basic_charts(df, fields):
    """
    自动生成几张基础图表。
    返回 [(标题, fig), ...]
    """
    charts = []

    numeric_cols = fields.get("numeric_cols", [])
    categorical_cols = fields.get("categorical_cols", [])
    date_cols = fields.get("date_cols", [])

    # 1. 缺失值图
    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False).head(10)

    if not missing.empty:
        fig, ax = plt.subplots()
        missing.plot(kind="bar", ax=ax)
        ax.set_title("Missing Values Top 10")
        ax.set_ylabel("Missing Count")
        ax.tick_params(axis="x", rotation=45)
        charts.append(("缺失值最多的字段 Top 10", fig))

    # 2. 第一个数值列分布图
    if numeric_cols:
        col = numeric_cols[0]
        fig, ax = plt.subplots()
        df[col].dropna().plot(kind="hist", bins=20, ax=ax)
        ax.set_title("Numeric Distribution")
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")
        charts.append((f"{col} 分布图", fig))

    # 3. 第一个分类列 Top 10
    if categorical_cols:
        col = categorical_cols[0]
        top_counts = df[col].value_counts().head(10)

        fig, ax = plt.subplots()
        top_counts.plot(kind="bar", ax=ax)
        ax.set_title("Category Top 10")
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=45)
        charts.append((f"{col} 出现次数 Top 10", fig))

    # 4. 第一个数值字段按日期变化趋势
    if date_cols and numeric_cols:
        date_col = date_cols[0]
        numeric_col = numeric_cols[0]

        temp = df.copy()
        temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")
        temp = temp.dropna(subset=[date_col])

        if not temp.empty:
            trend = temp.groupby(temp[date_col].dt.date)[numeric_col].sum()

            if len(trend) > 1:
                fig, ax = plt.subplots()
                trend.plot(kind="line", marker="o", ax=ax)
                ax.set_title("Numeric Trend 1")
                ax.set_xlabel("Date")
                ax.set_ylabel("Value")
                ax.tick_params(axis="x", rotation=45)
                charts.append((f"{numeric_col} 按日期变化趋势", fig))

    # 5. 第二个数值字段按日期变化趋势
    if date_cols and len(numeric_cols) >= 2:
        date_col = date_cols[0]
        numeric_col = numeric_cols[1]

        temp = df.copy()
        temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")
        temp = temp.dropna(subset=[date_col])

        if not temp.empty:
            trend = temp.groupby(temp[date_col].dt.date)[numeric_col].sum()

            if len(trend) > 1:
                fig, ax = plt.subplots()
                trend.plot(kind="line", marker="o", ax=ax)
                ax.set_title("Numeric Trend 2")
                ax.set_xlabel("Date")
                ax.set_ylabel("Value")
                ax.tick_params(axis="x", rotation=45)
                charts.append((f"{numeric_col} 按日期变化趋势", fig))

    return charts
