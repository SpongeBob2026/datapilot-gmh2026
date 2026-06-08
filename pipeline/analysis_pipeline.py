from core.field_detector import detect_fields
from core.basic_analysis import get_overview, get_column_quality, get_numeric_summary
from core.anomaly_detector import detect_numeric_anomalies
from core.correlation_analysis import get_correlation_matrix, get_strong_correlations
from core.chart_recommender import recommend_charts
from core.cleaning_advisor import generate_cleaning_suggestions


def run_general_analysis(df):
    """
    通用表格分析主流程。

    输入：
        df: pandas DataFrame

    输出：
        analysis_result: dict
        统一保存本次分析产生的所有结果。

    设计原则：
        1. app.py 不直接调用各个分析模块。
        2. 所有分析结果统一从这里生成。
        3. 后续新增分析功能时，优先扩展这里，而不是改 app.py。
    """

    fields = detect_fields(df)
    overview = get_overview(df)
    column_quality = get_column_quality(df)
    numeric_summary = get_numeric_summary(df)
    anomaly_summary = detect_numeric_anomalies(df)
    correlation_matrix = get_correlation_matrix(df)
    strong_correlations = get_strong_correlations(df)
    chart_recommendations = recommend_charts(df, fields)

    cleaning_suggestions = generate_cleaning_suggestions(
        df=df,
        overview=overview,
        column_quality=column_quality,
        anomaly_summary=anomaly_summary,
        fields=fields
    )

    analysis_result = {
        "df": df,
        "fields": fields,
        "overview": overview,
        "column_quality": column_quality,
        "numeric_summary": numeric_summary,
        "anomaly_summary": anomaly_summary,
        "correlation_matrix": correlation_matrix,
        "strong_correlations": strong_correlations,
        "chart_recommendations": chart_recommendations,
        "cleaning_suggestions": cleaning_suggestions,
    }

    return analysis_result


def get_analysis_status(analysis_result):
    """
    根据分析结果生成当前数据的状态提示。

    这个函数后面会用于工作台左侧状态栏，例如：
    ✅ 文件已读取
    ✅ 字段已识别
    ⚠️ 检测到异常值
    ✅ 已生成清洗建议
    """

    status = []

    df = analysis_result.get("df")
    overview = analysis_result.get("overview", {})
    fields = analysis_result.get("fields", {})
    anomaly_summary = analysis_result.get("anomaly_summary")
    cleaning_suggestions = analysis_result.get("cleaning_suggestions")
    correlation_matrix = analysis_result.get("correlation_matrix")

    if df is not None and not df.empty:
        status.append({
            "状态": "成功",
            "说明": "文件已读取"
        })

    if fields:
        status.append({
            "状态": "成功",
            "说明": "字段已识别"
        })

    if overview.get("缺失值总数", 0) > 0:
        status.append({
            "状态": "提醒",
            "说明": "存在缺失值"
        })
    else:
        status.append({
            "状态": "成功",
            "说明": "未发现缺失值"
        })

    if overview.get("重复行数", 0) > 0:
        status.append({
            "状态": "提醒",
            "说明": "存在重复行"
        })
    else:
        status.append({
            "状态": "成功",
            "说明": "未发现重复行"
        })

    if anomaly_summary is not None and not anomaly_summary.empty:
        high_risk = anomaly_summary[anomaly_summary["异常值数量"] > 0]

        if not high_risk.empty:
            status.append({
                "状态": "提醒",
                "说明": "检测到异常值"
            })
        else:
            status.append({
                "状态": "成功",
                "说明": "未发现明显异常值"
            })

    if correlation_matrix is not None and not correlation_matrix.empty:
        status.append({
            "状态": "成功",
            "说明": "已完成相关性分析"
        })

    if cleaning_suggestions is not None and not cleaning_suggestions.empty:
        status.append({
            "状态": "成功",
            "说明": "已生成清洗建议"
        })

    return status
