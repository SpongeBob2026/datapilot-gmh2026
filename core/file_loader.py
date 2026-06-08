import pandas as pd


def load_uploaded_file(uploaded_file):
    """
    读取用户上传的 CSV 或 Excel 文件，并做最基础清洗。
    """
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        try:
            df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding="gbk")

    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file, engine="openpyxl")

    else:
        raise ValueError("暂时只支持 CSV 和 XLSX 文件。")

    # 清理列名两边的空格
    df.columns = [str(col).strip() for col in df.columns]

    # 删除全空行、全空列
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    return df