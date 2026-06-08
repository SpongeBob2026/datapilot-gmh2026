import streamlit as st

from pipeline.report_context import build_report_prompt
from utils.deepseek_client import call_deepseek


def load_prompt_template(prompt_path="prompts/general_report_prompt.txt"):
    """
    读取 AI 报告提示词模板。
    """
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def render_report_section(file_name, analysis_result):
    """
    渲染 AI 分析报告区域。

    输入：
        file_name: 上传文件名
        analysis_result: pipeline/analysis_pipeline.py 返回的统一分析结果

    作用：
        1. 读取提示词模板
        2. 构建 AI 报告 prompt
        3. 调用 DeepSeek 生成报告
        4. 展示报告结果

    设计原则：
        app.py 不直接负责 AI 报告生成细节。
    """

    st.subheader("AI 分析报告")

    st.info(
        "为了降低 API 成本和隐私风险，AI 只会读取统计摘要，"
        "不会读取完整原始表格。"
    )

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

    if st.button("生成 AI 数据分析报告"):
        with st.spinner("正在生成分析报告..."):
            try:
                prompt_template = load_prompt_template()
                prompt = build_report_prompt(
                    file_name=file_name,
                    analysis_result=analysis_result,
                    prompt_template=prompt_template + extra_instruction
                )

                report = call_deepseek(prompt)
                st.markdown(report)

                st.download_button(
                    label="下载 Markdown 报告",
                    data=report,
                    file_name="datapilot_report.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"AI 报告生成失败：{e}")
                st.warning(
                    "请检查 DeepSeek API Key、模型名称、账户余额和网络连接是否正常。"
                )
