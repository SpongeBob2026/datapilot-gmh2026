import streamlit as st

from config import APP_STAGE, APP_VERSION
from pipeline.analysis_pipeline import get_analysis_status


def render_sidebar(file_name=None, analysis_result=None):
    """
    渲染 DataPilot 左侧边栏。

    作用：
        1. 显示产品名称
        2. 显示分析模式
        3. 显示当前文件
        4. 显示数据状态
        5. 显示版本信息

    设计原则：
        app.py 不负责维护侧边栏细节。
        后续增加登录、历史记录、多分析模式时，优先修改本文件。
    """

    st.sidebar.title("DataPilot")

    st.sidebar.caption("AI 数据分析工作台")

    st.sidebar.markdown("---")

    st.sidebar.markdown("### 分析模式")

    mode = st.sidebar.radio(
        "请选择分析模式",
        ["通用表格分析"],
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")

    st.sidebar.markdown("### 当前文件")

    if file_name:
        st.sidebar.success(file_name)
    else:
        st.sidebar.info("尚未上传文件")

    st.sidebar.markdown("---")

    st.sidebar.markdown("### 数据状态")

    if analysis_result is None:
        st.sidebar.info("等待上传数据")
    else:
        status_list = get_analysis_status(analysis_result)

        for item in status_list:
            status_type = item.get("状态")
            message = item.get("说明")

            if status_type == "成功":
                st.sidebar.success(f"✅ {message}")
            elif status_type == "提醒":
                st.sidebar.warning(f"⚠️ {message}")
            else:
                st.sidebar.info(message)

    st.sidebar.markdown("---")

    st.sidebar.markdown("### 版本信息")
    st.sidebar.caption(f"当前版本：{APP_VERSION}")
    st.sidebar.caption("结构：主入口 + pipeline + sections")
    st.sidebar.caption(f"阶段：{APP_STAGE}")

    return mode
