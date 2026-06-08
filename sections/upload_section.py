import streamlit as st


def render_upload_section():
    """
    渲染醒目的文件上传区域。
    """

    st.markdown(
        """
        <style>
        div[data-testid="stFileUploader"] {
            margin-top: 0.5rem;
            margin-bottom: 1.5rem;
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
            margin-bottom: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="upload-panel-title">上传数据文件</div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "上传 CSV 或 Excel 文件",
        type=["csv", "xlsx"],
        label_visibility="collapsed"
    )

    return uploaded_file
