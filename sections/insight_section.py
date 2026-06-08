import streamlit as st


def render_insight_section(analysis_result):
    """
    渲染工作台初步洞察区域。

    作用：
        1. 根据字段结构判断适合的分析方向
        2. 根据缺失值、重复值、异常值生成风险提醒
        3. 给用户一个进入详细分析前的快速判断
    """

    overview = analysis_result.get("overview", {})
    fields = analysis_result.get("fields", {})
    anomaly_summary = analysis_result.get("anomaly_summary")
    strong_correlations = analysis_result.get("strong_correlations")
    cleaning_suggestions = analysis_result.get("cleaning_suggestions")
    chart_recommendations = analysis_result.get("chart_recommendations")

    numeric_cols = fields.get("numeric_cols", [])
    date_cols = fields.get("date_cols", [])
    categorical_cols = fields.get("categorical_cols", [])
    text_cols = fields.get("text_cols", [])

    st.subheader("AI 初步洞察")

    insight_items = []
    risk_items = []
    next_steps = []

    # 1. 样本量判断
    row_count = overview.get("行数", 0)

    if row_count < 30:
        risk_items.append("样本量较小，当前结论更适合做初步观察，不适合直接下强结论。")
    elif row_count < 200:
        insight_items.append("数据量适中，可以进行基础统计、分组对比和趋势观察。")
    else:
        insight_items.append("数据量较充足，可以进一步做分组分析、趋势分析和异常检测。")

    # 2. 字段结构判断
    if date_cols and numeric_cols:
        insight_items.append("数据中同时包含日期字段和数值字段，适合进行时间趋势分析。")
        next_steps.append("优先查看“图表分析”中的趋势图，观察核心数值是否随时间发生明显变化。")

    if categorical_cols and numeric_cols:
        insight_items.append("数据中同时包含分类字段和数值字段，适合进行分组对比分析。")
        next_steps.append("查看不同分类下的数值差异，例如不同商品、城市或类别之间的表现。")

    if len(numeric_cols) >= 2:
        insight_items.append("数据中包含多个数值字段，可以进行相关性分析。")
        next_steps.append("查看“图表分析”中的相关性矩阵，判断数值字段之间是否同步变化。")

    if text_cols:
        insight_items.append("数据中包含文本字段，后续可以扩展关键词分析、文本长度分析或用户反馈分析。")

    # 3. 缺失值与重复值判断
    missing_total = overview.get("缺失值总数", 0)
    duplicate_rows = overview.get("重复行数", 0)

    if missing_total > 0:
        risk_items.append(f"当前数据存在 {missing_total} 个缺失值，建议在正式分析前检查缺失字段。")

    if duplicate_rows > 0:
        risk_items.append(f"当前数据存在 {duplicate_rows} 条重复行，建议核查是否为真实重复记录。")

    # 4. 异常值判断
    if anomaly_summary is not None and not anomaly_summary.empty:
        high_risk = anomaly_summary[anomaly_summary["异常值数量"] > 0]

        if not high_risk.empty:
            anomaly_cols = high_risk["字段名"].tolist()
            risk_items.append(
                "检测到异常值字段：" + "、".join(anomaly_cols) + "。建议优先核查这些字段。"
            )
            next_steps.append("进入“数据质量”模块，查看异常值检测和清洗建议。")

    # 5. 强相关判断
    if strong_correlations is not None and not strong_correlations.empty:
        insight_items.append("检测到较强相关字段对，可以进一步结合业务背景判断其含义。")
        next_steps.append("查看“图表分析”中的强相关字段对，但不要直接把相关性理解为因果关系。")

    # 6. 图表推荐判断
    if chart_recommendations is not None and not chart_recommendations.empty:
        next_steps.append("根据“图表推荐”结果，优先查看折线图、柱状图、直方图和散点图。")

    # 7. 清洗建议判断
    if cleaning_suggestions is not None and not cleaning_suggestions.empty:
        high_priority = cleaning_suggestions[cleaning_suggestions["优先级"] == "高"]

        if not high_priority.empty:
            risk_items.append("存在高优先级清洗问题，建议先处理数据质量，再生成正式报告。")

    # 兜底提示
    if not insight_items:
        insight_items.append("当前数据结构较简单，适合先进行数据预览、字段检查和基础统计。")

    if not next_steps:
        next_steps.append("建议先查看数据详情，再根据字段结构决定是否继续做图表、质量检查或 AI 报告。")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 适合的分析方向")

        for item in insight_items:
            st.success(item)

    with col2:
        st.markdown("### 需要注意的问题")

        if risk_items:
            for item in risk_items:
                st.warning(item)
        else:
            st.success("当前未发现明显高风险问题，可以继续进行后续分析。")

    st.markdown("### 建议下一步")

    for index, step in enumerate(next_steps, start=1):
        st.write(f"{index}. {step}")
