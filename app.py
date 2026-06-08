import streamlit as st

from core.file_loader import load_uploaded_file
from pipeline.analysis_pipeline import run_general_analysis

from sections.sidebar_section import render_sidebar
from sections.home_section import render_home_page
from sections.upload_section import render_upload_section
from sections.workspace_section import render_workspace


st.set_page_config(
    page_title="DataPilot 数据分析工作台",
    page_icon="🌈",
    layout="wide"
)





def main():
    """
    DataPilot 主入口。

    app.py 的职责：
        1. 配置页面
        2. 上传文件
        3. 调用统一分析流程
        4. 调用页面模块渲染
    """

    render_home_page()

    uploaded_file = render_upload_section()

    if uploaded_file is None:
        render_sidebar()
        return

    try:
        df = load_uploaded_file(uploaded_file)
    except Exception as e:
        render_sidebar(file_name=uploaded_file.name)
        st.error(f"文件读取失败：{e}")
        st.stop()

    if df.empty:
        render_sidebar(file_name=uploaded_file.name)
        st.error("文件读取成功，但数据为空。")
        st.stop()

    analysis_result = run_general_analysis(df)

    render_sidebar(
        file_name=uploaded_file.name,
        analysis_result=analysis_result
    )

    render_workspace(
        file_name=uploaded_file.name,
        analysis_result=analysis_result
    )


if __name__ == "__main__":
    main()
