import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_secret_value(key, default=None):
    """
    优先从 Streamlit secrets 读取配置；
    如果没有，再从 .env / 环境变量读取。
    这样本地开发和 Streamlit Cloud 部署都能兼容。
    """
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    return os.getenv(key, default)


def get_deepseek_client():
    api_key = get_secret_value("DEEPSEEK_API_KEY")

    if not api_key:
        raise ValueError(
            "没有找到 DEEPSEEK_API_KEY。请在本地 .env 或 Streamlit Secrets 中配置。"
        )

    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )


def call_deepseek(prompt, temperature=0.3):
    client = get_deepseek_client()
    model = get_secret_value("DEEPSEEK_MODEL", "deepseek-chat")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "你是一个专业的数据分析助手，擅长解释表格数据、发现异常、总结趋势，并给出清晰可执行的建议。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature,
    )

    return response.choices[0].message.content
