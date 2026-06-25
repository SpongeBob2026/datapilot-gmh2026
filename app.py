import streamlit as st

from core.file_loader import load_uploaded_file, load_local_file
from pipeline.analysis_pipeline import run_general_analysis

from sections.sidebar_section import render_sidebar
from sections.home_section import render_home_page
from sections.upload_section import render_upload_section
from sections.privacy_notice_section import render_privacy_notice
from sections.workspace_section import render_workspace
from utils.error_handler import (
    show_analysis_error,
    show_empty_data_error,
    show_file_read_error,
    show_sample_data_error,
)


st.set_page_config(
    page_title="DataPilot 数据分析工作台",
    layout="wide"
)


def main():
    """
    DataPilot 主入口。

    app.py 的职责：
        1. 配置页面
        2. 渲染首页
        3. 处理文件上传或示例数据
        4. 调用统一分析流程
        5. 调用页面模块渲染
    """

    render_home_page()

    render_privacy_notice()

    uploaded_file, use_sample = render_upload_section()

    if uploaded_file is None and not use_sample:
        render_sidebar()
        return

    if use_sample and uploaded_file is None:
        file_name = "sales_sample.csv"

        try:
            df = load_local_file("sample_data/sales_sample.csv")
        except Exception as e:
            render_sidebar(file_name=file_name)
            show_sample_data_error(e)
            st.stop()

    else:
        file_name = uploaded_file.name

        try:
            df = load_uploaded_file(uploaded_file)
        except Exception as e:
            render_sidebar(file_name=file_name)
            show_file_read_error(e)
            st.stop()

    if df.empty:
        render_sidebar(file_name=file_name)
        show_empty_data_error()
        st.stop()

    try:
        analysis_result = run_general_analysis(df)
    except Exception as e:
        render_sidebar(file_name=file_name)
        show_analysis_error(e)
        st.stop()

    render_sidebar(
        file_name=file_name,
        analysis_result=analysis_result
    )

    render_workspace(
        file_name=file_name,
        analysis_result=analysis_result
    )


if __name__ == "__main__":
    main()
