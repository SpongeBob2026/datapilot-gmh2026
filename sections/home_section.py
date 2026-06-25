import streamlit as st

from config import APP_VERSION


def render_home_page():
    """
    极简首页。

    目标：
        1. 保留产品名称
        2. 保留一句核心说明
        3. 不显示多余功能介绍
    """

    st.title(f"DataPilot：AI 数据分析工作台 {APP_VERSION}")
    st.caption("上传 Excel / CSV，自动生成数据概览、质量检查、图表分析和中文分析报告。")
