import streamlit as st


def render_upload_section():
    """
    渲染醒目的文件上传区域。

    返回：
        uploaded_file: 用户上传的文件
        use_sample: 是否使用示例数据
    """

    st.markdown(
        """
        <style>
        div[data-testid="stFileUploader"] {
            margin-top: 0.5rem;
            margin-bottom: 1rem;
        }

        div[data-testid="stFileUploader"] section {
            min-height: 150px;
            border: 2px dashed #B8C0CC;
            border-radius: 18px;
            background: rgba(250, 250, 250, 0.75);
            padding: 26px;
        }

        div[data-testid="stFileUploader"] section:hover {
            border-color: #6C8CFF;
            background: rgba(245, 248, 255, 0.95);
        }

        div[data-testid="stFileUploader"] button {
            min-height: 46px;
            padding-left: 22px;
            padding-right: 22px;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 600;
        }

        .upload-panel-title {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .upload-panel-desc {
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="upload-panel-title">开始分析</div>
        <div class="upload-panel-desc">上传 CSV / XLSX，或使用内置示例数据体验完整流程。</div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "上传 CSV 或 Excel 文件",
        type=["csv", "xlsx"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        st.session_state["use_sample_data"] = False

    col1, col2 = st.columns([1, 3])

    with col1:
        if st.button("体验示例数据", use_container_width=True):
            st.session_state["use_sample_data"] = True

    with col2:
        if st.session_state.get("use_sample_data", False) and uploaded_file is None:
            st.success("已选择销售示例数据。上传新文件后会自动切换为你的数据。")
        else:
            st.caption("没有数据文件时，可先用销售示例数据体验公开测试版。")

    with st.expander("文件要求", expanded=False):
        st.markdown(
            """
            - 支持 `.csv` 和 `.xlsx` 文件。
            - 表格第一行建议作为字段名，例如：日期、商品、销售额、订单数。
            - 尽量避免合并单元格、多层表头、空白标题列。
            - 暂不支持 PDF、Word、图片和数据库直连。
            - 请勿上传身份证号、手机号、银行卡号、真实客户名单等敏感数据。
            """
        )

    use_sample = st.session_state.get("use_sample_data", False)

    return uploaded_file, use_sample
