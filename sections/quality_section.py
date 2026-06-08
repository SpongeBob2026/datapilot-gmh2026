import streamlit as st


def render_quality_section(analysis_result):
    """
    渲染数据质量区域。

    输入：
        analysis_result: pipeline/analysis_pipeline.py 返回的统一分析结果

    作用：
        1. 展示异常值检测结果
        2. 展示数据清洗建议
        3. 提醒用户优先处理高风险问题
    """

    anomaly_summary = analysis_result.get("anomaly_summary")
    cleaning_suggestions = analysis_result.get("cleaning_suggestions")

    st.subheader("数据质量与清洗建议")

    tab1, tab2 = st.tabs([
        "异常值检测",
        "清洗建议"
    ])

    with tab1:
        st.markdown("### 异常值检测")
        st.info("当前使用 IQR 四分位距方法检测数值字段异常值。异常值不一定是错误数据，需要结合业务背景判断。")

        if anomaly_summary is None or anomaly_summary.empty:
            st.success("当前数据中没有检测到明显的数值异常，或数值字段数量不足。")
        else:
            st.dataframe(anomaly_summary, use_container_width=True)

            high_risk = anomaly_summary[anomaly_summary["异常值数量"] > 0]

            if high_risk.empty:
                st.success("数值字段未发现明显异常值。")
            else:
                st.warning("以下字段检测到异常值，建议优先核查：")
                st.dataframe(high_risk, use_container_width=True)

                st.markdown("#### 处理建议")
                st.write(
                    "异常值可能来自录入错误、真实极端业务情况、促销活动、采集异常等。"
                    "建议先核查原始记录，不要直接删除。"
                )

    with tab2:
        st.markdown("### 数据清洗建议")
        st.info("系统会根据重复值、缺失值、异常值、日期字段和分类字段自动生成清洗建议。")

        if cleaning_suggestions is None or cleaning_suggestions.empty:
            st.success("当前数据暂未发现明显需要清洗的问题。")
        else:
            st.dataframe(cleaning_suggestions, use_container_width=True)

            high_priority = cleaning_suggestions[cleaning_suggestions["优先级"] == "高"]
            medium_priority = cleaning_suggestions[cleaning_suggestions["优先级"] == "中"]

            if not high_priority.empty:
                st.warning("高优先级清洗问题：")
                st.dataframe(high_priority, use_container_width=True)

            if not medium_priority.empty:
                st.info("中优先级清洗建议：")
                st.dataframe(medium_priority, use_container_width=True)

            st.markdown("#### 清洗原则")
            st.write(
                "清洗数据前应先确认业务含义。对于异常值和缺失值，优先核查来源，"
                "再决定删除、填补、标记或保留。"
            )
