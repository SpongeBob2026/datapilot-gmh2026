import streamlit as st


def render_privacy_notice():
    """
    渲染隐私与使用提醒。

    作用：
        1. 提醒用户不要上传敏感数据
        2. 说明 AI 报告只读取统计摘要
        3. 提醒 AI 报告会消耗 API 额度
    """

    with st.expander("使用前提醒", expanded=False):
        st.markdown(
            """
            - 请勿上传身份证号、手机号、银行卡号、真实客户名单等敏感数据。
            - AI 报告只读取统计摘要，不直接读取完整原始表格。
            - 点击生成 AI 报告会调用 DeepSeek API，并消耗 API 额度。
            - 当前版本主要用于学习、测试和基础数据分析，不适合作为正式商业决策的唯一依据。
            """
        )
