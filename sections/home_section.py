import streamlit as st


def render_home_page():
    """
    极简首页。

    目标：
        1. 保留产品名称
        2. 保留一句核心说明
        3. 不显示多余功能介绍
    """

    st.title("🌈 DataPilot：AI 数据分析工作台 v0.6")
    st.caption("上传 Excel / CSV，自动生成数据分析结果。")
