import streamlit as st

from core.chart_generator import generate_basic_charts


def render_chart_section(analysis_result):
    """
    渲染图表分析区域。

    输入：
        analysis_result: pipeline/analysis_pipeline.py 返回的统一分析结果

    作用：
        1. 展示自动生成图表
        2. 展示图表推荐
        3. 展示相关性分析结果
    """

    df = analysis_result.get("df")
    fields = analysis_result.get("fields", {})
    chart_recommendations = analysis_result.get("chart_recommendations")
    correlation_matrix = analysis_result.get("correlation_matrix")
    strong_correlations = analysis_result.get("strong_correlations")

    st.subheader("图表与相关性分析")

    tab1, tab2, tab3 = st.tabs([
        "自动图表",
        "图表推荐",
        "相关性分析"
    ])

    with tab1:
        st.markdown("### 自动生成图表")
        st.info("系统会根据字段类型自动生成基础图表，用于快速观察数据分布、趋势和类别差异。")

        if df is None or df.empty:
            st.warning("当前没有可用于绘图的数据。")
        else:
            charts = generate_basic_charts(df, fields)

            if not charts:
                st.info("当前数据暂时没有生成合适的基础图表。")
            else:
                for title, fig in charts:
                    st.markdown(f"#### {title}")
                    st.pyplot(fig)

    with tab2:
        st.markdown("### 图表推荐")
        st.info("系统会根据字段类型推荐适合的图表类型，帮助判断这份数据适合怎么分析。")

        if chart_recommendations is None or chart_recommendations.empty:
            st.info("当前数据字段不足，暂时无法生成图表推荐。")
        else:
            st.dataframe(chart_recommendations, width="stretch")

            st.markdown("#### 使用建议")
            st.write(
                "优先查看与日期字段和核心数值字段相关的折线图，用于判断趋势；"
                "再查看分类字段与数值字段的柱状图，用于比较不同类别之间的差异；"
                "最后查看数值字段的直方图和散点图，用于观察分布、异常值和相关关系。"
            )

    with tab3:
        st.markdown("### 相关性分析")
        st.info("当前使用 Pearson 相关系数分析数值字段之间的线性相关关系。相关性不等于因果关系。")

        if correlation_matrix is None or correlation_matrix.empty:
            st.info("当前数据中的数值字段少于 2 个，无法进行相关性分析。")
        else:
            st.markdown("#### 数值字段相关系数矩阵")
            st.dataframe(correlation_matrix, width="stretch")

            st.markdown("#### 强相关字段对")

            if strong_correlations is None or strong_correlations.empty:
                st.info("暂未发现绝对值大于等于 0.7 的强相关字段对。")
            else:
                st.dataframe(strong_correlations, width="stretch")

                st.markdown("#### 解读提醒")
                st.write(
                    "强相关说明两个数值字段在当前样本中存在同步变化关系，"
                    "但不能直接说明其中一个字段导致另一个字段变化。"
                    "需要结合业务背景、样本量和其他影响因素进一步判断。"
                )
