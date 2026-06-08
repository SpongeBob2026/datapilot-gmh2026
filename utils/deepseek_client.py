import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_deepseek_client():
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        raise ValueError("没有找到 DEEPSEEK_API_KEY，请检查 .env 文件。")

    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )


def call_deepseek(prompt, temperature=0.3):
    client = get_deepseek_client()
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

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