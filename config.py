APP_NAME = "DataPilot"
APP_VERSION = "v2.0"
APP_STAGE = "场景化分析基础版"

ANALYSIS_MODES = [
    "通用表格分析",
    "问卷数据分析",
    "小微商家经营分析",
    "个人消费分析",
    "数据分析学习陪练",
]

SAMPLE_DATASETS = {
    "sales": {
        "label": "销售示例数据",
        "file_name": "sales_sample.csv",
        "path": "sample_data/sales_sample.csv",
        "mode": "小微商家经营分析",
    },
    "survey": {
        "label": "问卷示例数据",
        "file_name": "survey_sample.csv",
        "path": "sample_data/survey_sample.csv",
        "mode": "问卷数据分析",
    },
    "expense": {
        "label": "消费示例数据",
        "file_name": "expense_sample.csv",
        "path": "sample_data/expense_sample.csv",
        "mode": "个人消费分析",
    },
}
