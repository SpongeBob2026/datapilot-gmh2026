import streamlit as st


def render_scenario_section(analysis_result):
    """
    渲染 v2.0 场景化分析结果。
    """
    scenario_result = analysis_result.get("scenario_result", {})
    analysis_mode = analysis_result.get("analysis_mode", "通用表格分析")

    st.subheader("场景分析")

    if analysis_mode == "通用表格分析":
        st.info("当前使用通用表格分析。可在左侧切换到问卷、经营、消费或学习陪练场景。")
        return

    st.caption(scenario_result.get("场景说明", ""))

    insight_df = scenario_result.get("洞察列表")

    if insight_df is None or insight_df.empty:
        st.info("当前数据暂未生成明确的场景化洞察。")
        return

    high_priority = insight_df[insight_df["优先级"] == "高"]

    if not high_priority.empty:
        st.markdown("### 优先关注")
        for _, row in high_priority.iterrows():
            st.warning(f"{row['分析维度']}：{row['发现']} 建议：{row['建议']}")

    st.markdown("### 场景洞察明细")
    st.dataframe(insight_df, width="stretch")

    st.markdown("### 使用建议")
    if analysis_mode == "问卷数据分析":
        st.write("优先查看样本量、满意度评分、选择题分布和开放反馈，再决定是否需要补充调研。")
    elif analysis_mode == "小微商家经营分析":
        st.write("优先查看销售额、订单量、客单价、商品或渠道贡献，以及异常波动日期。")
    elif analysis_mode == "个人消费分析":
        st.write("优先查看总支出、消费分类、大额消费和月度节奏，再制定预算调整计划。")
    elif analysis_mode == "数据分析学习陪练":
        st.write("按字段结构、数据质量、基础统计、图表观察、结论表达的顺序练习。")
