import json


def dataframe_to_records(df, limit=30):
    """
    将 DataFrame 安全转换为 records 格式。
    如果 DataFrame 为空，返回空列表。
    """
    if df is None or df.empty:
        return []

    return df.head(limit).to_dict(orient="records")


def dataframe_to_index_dict(df, limit=20):
    """
    将 DataFrame 安全转换为 index dict 格式。
    适合数值描述统计、相关性矩阵等表格。
    """
    if df is None or df.empty:
        return {}

    return df.head(limit).to_dict(orient="index")


def build_report_context(file_name, analysis_result):
    """
    构建 AI 分析报告所需的统计摘要。

    输入：
        file_name: 上传文件名
        analysis_result: analysis_pipeline.py 生成的统一分析结果

    输出：
        report_context: dict
        只包含统计摘要，不包含完整原始数据，降低 API 成本和隐私风险。
    """

    overview = analysis_result.get("overview", {})
    fields = analysis_result.get("fields", {})
    column_quality = analysis_result.get("column_quality")
    numeric_summary = analysis_result.get("numeric_summary")
    anomaly_summary = analysis_result.get("anomaly_summary")
    correlation_matrix = analysis_result.get("correlation_matrix")
    strong_correlations = analysis_result.get("strong_correlations")
    chart_recommendations = analysis_result.get("chart_recommendations")
    cleaning_suggestions = analysis_result.get("cleaning_suggestions")

    report_context = {
        "文件名": file_name,
        "数据概况": overview,
        "字段识别": fields,
        "字段质量": dataframe_to_records(column_quality, limit=30),
        "数值统计": dataframe_to_index_dict(numeric_summary, limit=20),
        "异常值检测": dataframe_to_records(anomaly_summary, limit=20),
        "相关性矩阵": dataframe_to_index_dict(correlation_matrix, limit=20),
        "强相关字段对": dataframe_to_records(strong_correlations, limit=20),
        "图表推荐": dataframe_to_records(chart_recommendations, limit=20),
        "数据清洗建议": dataframe_to_records(cleaning_suggestions, limit=30),
    }

    return report_context


def build_report_prompt(file_name, analysis_result, prompt_template):
    """
    根据提示词模板和分析结果，生成最终发送给 AI 的 prompt。
    """

    report_context = build_report_context(
        file_name=file_name,
        analysis_result=analysis_result
    )

    prompt = prompt_template + "\n\n以下是数据统计摘要：\n" + json.dumps(
        report_context,
        ensure_ascii=False,
        indent=2
    )

    return prompt
