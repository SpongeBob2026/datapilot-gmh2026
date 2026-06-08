import streamlit as st

from pipeline.report_context import build_report_prompt
from utils.deepseek_client import call_deepseek
from utils.error_handler import show_ai_report_error


def load_prompt_template(prompt_path="prompts/general_report_prompt.txt"):
    """
    读取 AI 报告提示词模板。
    """
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def render_report_section(file_name, analysis_result):
    """
    渲染 AI 分析报告区域。

    作用：
        1. 选择报告类型
        2. 构建 AI 报告 prompt
        3. 调用 DeepSeek 生成报告
        4. 将报告保存在 session_state 中
        5. 提供 Markdown 下载和手动复制区域
    """

    st.subheader("AI 分析报告")

    st.info(
        "AI 只读取统计摘要，不读取完整原始表格。生成报告会消耗 API 额度。"
    )

    report_key = f"report_{file_name}"

    report_type = st.radio(
        "请选择报告类型",
        ["详细分析报告", "简版分析报告"],
        horizontal=True
    )

    if report_type == "详细分析报告":
        extra_instruction = (
            "\n\n请生成一份较完整的数据分析报告，包含数据概况、字段结构、"
            "数据质量、异常值、相关性、图表推荐、风险提示和下一步建议。"
        )
    else:
        extra_instruction = (
            "\n\n请生成一份简版数据分析报告，重点说明数据概况、主要问题、"
            "关键发现和 3 条后续建议。避免过长。"
        )

    col1, col2 = st.columns([1, 3])

    with col1:
        generate_clicked = st.button(
            "生成 AI 数据分析报告",
            use_container_width=True
        )

    with col2:
        st.caption("建议先检查数据质量，再生成正式报告。")

    if generate_clicked:
        with st.spinner("正在生成分析报告..."):
            try:
                prompt_template = load_prompt_template()
                prompt = build_report_prompt(
                    file_name=file_name,
                    analysis_result=analysis_result,
                    prompt_template=prompt_template + extra_instruction
                )

                report = call_deepseek(prompt)
                st.session_state[report_key] = report

            except Exception as e:
                show_ai_report_error(e)

    report = st.session_state.get(report_key)

    if report:
        st.markdown("### 报告结果")
        st.markdown(report)

        st.download_button(
            label="下载 Markdown 报告",
            data=report,
            file_name="datapilot_report.md",
            mime="text/markdown",
            use_container_width=True
        )

        with st.expander("复制报告文本", expanded=False):
            st.text_area(
                "可以在这里全选复制报告内容",
                value=report,
                height=300
            )

    else:
        st.info("点击上方按钮后，系统会在这里显示 AI 分析报告。")
