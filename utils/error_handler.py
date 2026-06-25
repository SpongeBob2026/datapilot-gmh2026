import streamlit as st


def show_file_read_error(error):
    """
    显示文件读取失败提示。
    """
    st.error("文件读取失败。")

    st.markdown("可能原因：")
    st.write("1. 文件格式不受支持。当前仅支持 CSV 和 XLSX。")
    st.write("2. 文件内容为空。")
    st.write("3. CSV 编码不兼容。")
    st.write("4. Excel 文件损坏或表格结构异常。")

    with st.expander("查看技术错误信息", expanded=False):
        st.code(str(error))


def show_empty_data_error():
    """
    显示空数据提示。
    """
    st.error("文件读取成功，但没有有效数据。")

    st.markdown("请检查：")
    st.write("1. 表格是否为空。")
    st.write("2. 是否只有空行或空列。")
    st.write("3. 是否上传了错误的文件。")


def show_ai_report_error(error):
    """
    显示 AI 报告生成失败提示。
    """
    st.error("AI 报告生成失败。")

    st.markdown("可能原因：")
    st.write("1. DeepSeek API Key 未配置或已失效。")
    st.write("2. DeepSeek 账户余额不足。")
    st.write("3. 模型名称填写错误。")
    st.write("4. 网络连接失败。")
    st.write("5. 当前请求内容过长。")

    with st.expander("查看技术错误信息", expanded=False):
        st.code(str(error))


def show_analysis_error(error):
    """
    显示数据分析流程失败提示。
    """
    st.error("数据分析失败。")

    st.markdown("可能原因：")
    st.write("1. 字段类型过于复杂，系统无法自动识别。")
    st.write("2. 数据中存在无法计算的异常格式。")
    st.write("3. 文件行列结构不规则，例如多层表头或合并单元格。")
    st.write("4. 当前文件过大，浏览器或运行环境资源不足。")

    with st.expander("查看技术错误信息", expanded=False):
        st.code(str(error))


def show_sample_data_error(error):
    """
    显示示例数据读取失败提示。
    """
    st.error("示例数据读取失败。")

    st.markdown("请检查：")
    st.write("1. sample_data/sales_sample.csv 是否存在。")
    st.write("2. 示例数据文件是否被移动或删除。")
    st.write("3. 文件路径是否正确。")

    with st.expander("查看技术错误信息", expanded=False):
        st.code(str(error))
