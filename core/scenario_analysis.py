import pandas as pd


def _find_columns(columns, keywords):
    result = []
    for col in columns:
        text = str(col).lower()
        if any(keyword.lower() in text for keyword in keywords):
            result.append(col)
    return result


def _first_existing(columns, keywords):
    matches = _find_columns(columns, keywords)
    return matches[0] if matches else None


def _format_number(value):
    if pd.isna(value):
        return "暂无"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def _build_item(category, finding, suggestion, priority="中"):
    return {
        "分析维度": category,
        "发现": finding,
        "建议": suggestion,
        "优先级": priority,
    }


def analyze_scenario(df, fields, analysis_mode):
    if analysis_mode == "问卷数据分析":
        return analyze_survey(df, fields)
    if analysis_mode == "小微商家经营分析":
        return analyze_small_business(df, fields)
    if analysis_mode == "个人消费分析":
        return analyze_personal_expense(df, fields)
    if analysis_mode == "数据分析学习陪练":
        return analyze_learning_coach(df, fields)
    return {
        "场景名称": "通用表格分析",
        "场景说明": "适用于结构化表格的基础概览、质量检查、图表分析和 AI 报告。",
        "适配程度": "通用",
        "洞察列表": pd.DataFrame(),
    }


def analyze_survey(df, fields):
    items = []
    columns = df.columns.tolist()
    row_count = len(df)
    numeric_cols = fields.get("numeric_cols", [])
    categorical_cols = fields.get("categorical_cols", [])
    text_cols = fields.get("text_cols", [])

    satisfaction_cols = _find_columns(columns, ["满意", "评分", "分数", "score", "rating", "nps"])
    choice_cols = categorical_cols
    open_text_cols = text_cols

    if row_count < 30:
        items.append(_build_item(
            "样本量",
            f"当前共有 {row_count} 份记录，样本量偏小。",
            "适合作为初步反馈观察，不建议直接代表整体用户群体。",
            "高",
        ))
    else:
        items.append(_build_item(
            "样本量",
            f"当前共有 {row_count} 份记录，可用于基础分布和满意度观察。",
            "后续可以按人群、渠道或时间继续拆分对比。",
            "中",
        ))

    for col in satisfaction_cols[:3]:
        series = pd.to_numeric(df[col], errors="coerce")
        if series.notna().any():
            items.append(_build_item(
                "满意度/评分",
                f"{col} 平均值为 {_format_number(series.mean())}，中位数为 {_format_number(series.median())}。",
                "重点查看低分样本对应的人群、渠道或开放文本反馈。",
                "高",
            ))

    if choice_cols:
        items.append(_build_item(
            "选择题分布",
            "检测到可用于分组统计的选择题字段：" + "、".join(choice_cols[:5]) + "。",
            "优先查看各选项占比，找出最集中的需求、问题或偏好。",
            "中",
        ))

    if open_text_cols:
        items.append(_build_item(
            "开放题反馈",
            "检测到文本反馈字段：" + "、".join(open_text_cols[:5]) + "。",
            "建议后续扩展关键词提取、情绪倾向和典型意见归纳。",
            "中",
        ))

    if not items:
        items.append(_build_item(
            "场景适配",
            "当前字段暂未明显匹配问卷分析特征。",
            "建议包含评分、选择题、用户类型或开放反馈字段。",
            "中",
        ))

    return {
        "场景名称": "问卷数据分析",
        "场景说明": "关注样本量、选择题分布、满意度评分、开放题反馈和后续调研建议。",
        "适配程度": "已启用",
        "洞察列表": pd.DataFrame(items),
    }


def analyze_small_business(df, fields):
    items = []
    columns = df.columns.tolist()
    numeric_cols = fields.get("numeric_cols", [])
    date_cols = fields.get("date_cols", [])
    categorical_cols = fields.get("categorical_cols", [])

    sales_col = _first_existing(columns, ["销售额", "收入", "营收", "金额", "revenue", "sales", "amount"])
    order_col = _first_existing(columns, ["订单", "单量", "销量", "数量", "order", "quantity"])
    product_col = _first_existing(columns, ["商品", "产品", "品类", "类别", "product", "category"])
    city_col = _first_existing(columns, ["城市", "门店", "地区", "渠道", "city", "store", "channel"])

    if sales_col:
        sales = pd.to_numeric(df[sales_col], errors="coerce")
        items.append(_build_item(
            "经营规模",
            f"{sales_col} 合计为 {_format_number(sales.sum())}，平均每条记录为 {_format_number(sales.mean())}。",
            "优先结合日期、商品和城市字段查看收入来源结构。",
            "高",
        ))

    if order_col:
        orders = pd.to_numeric(df[order_col], errors="coerce")
        items.append(_build_item(
            "订单表现",
            f"{order_col} 合计为 {_format_number(orders.sum())}，平均每条记录为 {_format_number(orders.mean())}。",
            "可进一步计算客单价、转化效率或活动期间波动。",
            "中",
        ))

    if sales_col and order_col:
        sales = pd.to_numeric(df[sales_col], errors="coerce")
        orders = pd.to_numeric(df[order_col], errors="coerce").replace(0, pd.NA)
        avg_order_value = (sales / orders).dropna()
        if not avg_order_value.empty:
            items.append(_build_item(
                "客单价",
                f"估算客单价平均为 {_format_number(avg_order_value.mean())}。",
                "如果客单价波动明显，建议按商品、城市或活动日期拆分排查。",
                "中",
            ))

    for group_col in [product_col, city_col]:
        if group_col and sales_col:
            temp = df[[group_col, sales_col]].copy()
            temp[sales_col] = pd.to_numeric(temp[sales_col], errors="coerce")
            grouped = temp.groupby(group_col)[sales_col].sum().sort_values(ascending=False)
            if not grouped.empty:
                items.append(_build_item(
                    "分组贡献",
                    f"{group_col} 中贡献最高的是 {grouped.index[0]}，对应 {sales_col} 为 {_format_number(grouped.iloc[0])}。",
                    "建议重点分析头部贡献项，同时关注是否过度依赖单一来源。",
                    "中",
                ))

    if date_cols and numeric_cols:
        items.append(_build_item(
            "趋势分析",
            "检测到日期字段和数值字段，适合观察日/周/月趋势。",
            "优先查看收入、订单数是否存在活动峰值、淡旺季或异常波动。",
            "高",
        ))

    if not categorical_cols:
        items.append(_build_item(
            "字段结构",
            "当前缺少明显的商品、门店、渠道或客户分类字段。",
            "补充分组字段后，经营分析会更容易定位增长来源。",
            "中",
        ))

    if not items:
        items.append(_build_item(
            "场景适配",
            "当前字段暂未明显匹配小微商家经营分析特征。",
            "建议包含日期、销售额、订单数、商品、门店或渠道字段。",
            "中",
        ))

    return {
        "场景名称": "小微商家经营分析",
        "场景说明": "关注销售额、订单量、客单价、商品/门店贡献和经营波动。",
        "适配程度": "已启用",
        "洞察列表": pd.DataFrame(items),
    }


def analyze_personal_expense(df, fields):
    items = []
    columns = df.columns.tolist()
    date_cols = fields.get("date_cols", [])

    amount_col = _first_existing(columns, ["金额", "支出", "价格", "花费", "amount", "cost", "expense"])
    category_col = _first_existing(columns, ["类别", "分类", "用途", "商户", "项目", "category", "merchant"])
    account_col = _first_existing(columns, ["账户", "支付", "卡", "渠道", "account", "payment"])

    if amount_col:
        amount = pd.to_numeric(df[amount_col], errors="coerce")
        items.append(_build_item(
            "总支出",
            f"{amount_col} 合计为 {_format_number(amount.sum())}，平均每笔为 {_format_number(amount.mean())}。",
            "建议先确认金额字段是否全部为支出，避免收入和退款混在一起。",
            "高",
        ))

    if amount_col and category_col:
        temp = df[[category_col, amount_col]].copy()
        temp[amount_col] = pd.to_numeric(temp[amount_col], errors="coerce")
        grouped = temp.groupby(category_col)[amount_col].sum().sort_values(ascending=False)
        if not grouped.empty:
            items.append(_build_item(
                "消费结构",
                f"支出最高的 {category_col} 是 {grouped.index[0]}，合计 {_format_number(grouped.iloc[0])}。",
                "优先检查高支出分类是否符合预算预期。",
                "高",
            ))

    if amount_col:
        amount = pd.to_numeric(df[amount_col], errors="coerce")
        high_threshold = amount.quantile(0.9)
        high_count = int((amount >= high_threshold).sum()) if pd.notna(high_threshold) else 0
        items.append(_build_item(
            "大额消费",
            f"按当前数据估算，前 10% 大额消费阈值约为 {_format_number(high_threshold)}，共有 {high_count} 笔。",
            "建议逐笔核查大额消费是否为必要支出、周期账单或偶发支出。",
            "中",
        ))

    if date_cols and amount_col:
        items.append(_build_item(
            "时间节奏",
            "检测到日期和金额字段，适合观察日度或月度消费节奏。",
            "建议按月份汇总，识别消费高峰和预算超支时间段。",
            "中",
        ))

    if account_col:
        items.append(_build_item(
            "支付渠道",
            f"检测到支付或账户字段：{account_col}。",
            "可以按渠道对比支出，识别信用卡、储蓄卡或平台支付占比。",
            "低",
        ))

    if not items:
        items.append(_build_item(
            "场景适配",
            "当前字段暂未明显匹配个人消费分析特征。",
            "建议包含日期、金额、消费分类、商户或支付方式字段。",
            "中",
        ))

    return {
        "场景名称": "个人消费分析",
        "场景说明": "关注总支出、消费结构、大额消费、时间节奏和预算管理。",
        "适配程度": "已启用",
        "洞察列表": pd.DataFrame(items),
    }


def analyze_learning_coach(df, fields):
    items = []
    overview = {
        "数值字段": len(fields.get("numeric_cols", [])),
        "日期字段": len(fields.get("date_cols", [])),
        "分类字段": len(fields.get("categorical_cols", [])),
        "文本字段": len(fields.get("text_cols", [])),
    }

    items.append(_build_item(
        "学习路径",
        "建议按“看结构、查质量、找分布、做对比、看趋势、写结论”的顺序分析。",
        "先不要急着生成报告，先确认字段含义和数据质量。",
        "高",
    ))

    items.append(_build_item(
        "字段理解",
        "当前字段结构为：" + "，".join([f"{key} {value} 个" for key, value in overview.items()]) + "。",
        "根据字段类型选择分析方法：数值看统计，分类看占比，日期看趋势，文本看关键词。",
        "高",
    ))

    if fields.get("numeric_cols"):
        items.append(_build_item(
            "数值分析练习",
            "这份数据可以练习均值、中位数、极值、分布和异常值判断。",
            "先找出最大值和最小值，再判断它们是否符合业务常识。",
            "中",
        ))

    if fields.get("categorical_cols"):
        items.append(_build_item(
            "分组对比练习",
            "这份数据可以练习按分类字段做分组对比。",
            "选择一个分类字段和一个数值字段，比较不同组之间的差异。",
            "中",
        ))

    if fields.get("date_cols"):
        items.append(_build_item(
            "趋势分析练习",
            "这份数据可以练习按日期观察趋势。",
            "把日期字段作为横轴，观察核心数值是否存在上升、下降或峰值。",
            "中",
        ))

    return {
        "场景名称": "数据分析学习陪练",
        "场景说明": "把当前表格转化为学习材料，引导用户理解字段、质量、图表和结论。",
        "适配程度": "已启用",
        "洞察列表": pd.DataFrame(items),
    }
