# DataPilot 公开测试部署说明

推荐使用 Streamlit Cloud 部署公开测试版。

## 一、部署前检查

- GitHub 仓库已包含最新代码
- `.env` 不要上传到 GitHub
- `.streamlit/secrets.toml` 不要上传到 GitHub
- `requirements.txt` 已包含运行依赖
- `runtime.txt` 已指定 Python 版本

## 二、Streamlit Cloud 部署

1. 打开 Streamlit Cloud
2. 选择 GitHub 仓库：`SpongeBob2026/datapilot-gmh2026`
3. Branch 选择：`main`
4. Main file path 填写：`app.py`
5. 点击 Deploy

## 三、Secrets 配置

在 Streamlit Cloud 的 App settings -> Secrets 中填写：

```toml
DEEPSEEK_API_KEY = "你的 DeepSeek API Key"
DEEPSEEK_MODEL = "deepseek-chat"
```

保存后重启应用。

## 四、公开测试链接

部署成功后，Streamlit Cloud 会生成公网链接，格式通常类似：

```text
https://你的应用名.streamlit.app
```

把这个链接发给测试用户即可。

## 五、测试建议

公开测试时建议先让用户使用内置销售示例数据体验，再上传自己的 CSV / XLSX 文件。

提醒用户不要上传身份证号、手机号、银行卡号、真实客户名单等敏感数据。
