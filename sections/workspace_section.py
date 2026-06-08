import streamlit as st

from sections.overview_section import render_overview_section
from sections.insight_section import render_insight_section
from sections.data_detail_section import render_data_detail_section
from sections.quality_section import render_quality_section
from sections.chart_section import render_chart_section
from sections.report_section import render_report_section


def render_workspace(file_name, analysis_result):
    """
    渲染上传文件后的 DataPilot 工作台主界面。

    作用：
        1. 显示当前分析文件
        2. 展示数据概览
        3. 展示 AI 初步洞察
        4. 组织数据详情、数据质量、图表分析、AI 报告四个主模块

    设计原则：
        app.py 不维护工作台布局。
        后续页面布局调整，优先修改本文件。
    """

    st.caption(f"当前分析文件：{file_name}")

    st.markdown("---")

    render_overview_section(analysis_result)

    st.markdown("---")

    render_insight_section(analysis_result)

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "数据详情",
        "数据质量",
        "图表分析",
        "AI 报告"
    ])

    with tab1:
        render_data_detail_section(analysis_result)

    with tab2:
        render_quality_section(analysis_result)

    with tab3:
        render_chart_section(analysis_result)

    with tab4:
        render_report_section(file_name, analysis_result)
