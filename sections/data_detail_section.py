import streamlit as st


def render_data_detail_section(analysis_result):
    """
    渲染数据详情区域。

    输入：
        analysis_result: pipeline/analysis_pipeline.py 返回的统一分析结果

    作用：
        1. 展示原始数据预览
        2. 展示字段质量检查
        3. 展示数值字段描述统计
    """

    df = analysis_result.get("df")
    overview = analysis_result.get("overview", {})
    column_quality = analysis_result.get("column_quality")
    numeric_summary = analysis_result.get("numeric_summary")

    st.subheader("数据详情")

    tab1, tab2, tab3 = st.tabs([
        "数据预览",
        "字段质量",
        "基础统计"
    ])

    with tab1:
        st.markdown("### 数据预览")

        if df is None or df.empty:
            st.warning("当前没有可预览的数据。")
        else:
            st.dataframe(df.head(50), width="stretch")

            st.caption(
                f"当前仅展示前 50 行。完整数据共有 {overview.get('行数', 0)} 行，"
                f"{overview.get('列数', 0)} 列。"
            )

    with tab2:
        st.markdown("### 字段质量检查")

        if column_quality is None or column_quality.empty:
            st.info("暂无字段质量检查结果。")
        else:
            st.dataframe(column_quality, width="stretch")

            missing_total = overview.get("缺失值总数", 0)
            duplicate_rows = overview.get("重复行数", 0)

            if missing_total > 0 or duplicate_rows > 0:
                st.warning(
                    f"当前数据存在 {missing_total} 个缺失值，"
                    f"{duplicate_rows} 条重复行，建议在进一步分析前先核查。"
                )
            else:
                st.success("当前数据未发现明显缺失值或重复行问题。")

    with tab3:
        st.markdown("### 数值字段描述统计")

        if numeric_summary is None or numeric_summary.empty:
            st.info("当前数据中没有识别到数值字段。")
        else:
            st.dataframe(numeric_summary, width="stretch")

            st.caption(
                "说明：这里展示数值字段的非空数量、平均值、标准差、最小值、分位数和最大值。"
            )
