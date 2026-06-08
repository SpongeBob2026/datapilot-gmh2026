import streamlit as st


def render_overview_section(analysis_result):
    """
    渲染数据概览区域。

    输入：
        analysis_result: pipeline/analysis_pipeline.py 返回的统一分析结果

    作用：
        1. 显示数据基础指标
        2. 显示字段类型数量
        3. 为工作台页面提供顶部总览
    """

    overview = analysis_result.get("overview", {})
    fields = analysis_result.get("fields", {})

    numeric_cols = fields.get("numeric_cols", [])
    date_cols = fields.get("date_cols", [])
    categorical_cols = fields.get("categorical_cols", [])
    text_cols = fields.get("text_cols", [])

    st.subheader("数据概览")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("行数", overview.get("行数", 0))
    col2.metric("列数", overview.get("列数", 0))
    col3.metric("重复行数", overview.get("重复行数", 0))
    col4.metric("缺失值总数", overview.get("缺失值总数", 0))
    col5.metric("缺失值比例", overview.get("缺失值比例", 0))

    st.markdown("### 字段结构")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("数值字段", len(numeric_cols))
    c2.metric("日期字段", len(date_cols))
    c3.metric("分类字段", len(categorical_cols))
    c4.metric("文本字段", len(text_cols))

    with st.expander("查看字段识别详情", expanded=False):
        left, right = st.columns(2)

        with left:
            st.markdown("**数值字段**")
            st.write(numeric_cols if numeric_cols else "暂无")

            st.markdown("**日期字段**")
            st.write(date_cols if date_cols else "暂无")

        with right:
            st.markdown("**分类字段**")
            st.write(categorical_cols if categorical_cols else "暂无")

            st.markdown("**文本字段**")
            st.write(text_cols if text_cols else "暂无")
