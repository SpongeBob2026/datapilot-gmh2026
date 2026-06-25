# DataPilot 开发规范

本文档用于说明 DataPilot 项目的开发结构、模块职责和后续扩展规则。

核心原则：

后续新增功能时，尽量不要频繁修改 app.py。

---

## 一、总体开发原则

### 1. app.py 只做主入口

app.py 只负责：

- 页面配置
- 文件上传入口
- 文件读取
- 调用统一分析流程
- 调用侧边栏
- 调用工作台页面

app.py 不应该直接负责：

- 字段识别
- 异常值检测
- 相关性分析
- 图表推荐
- 数据清洗建议
- AI 报告上下文拼接
- 页面具体模块展示

---

## 二、目录职责

### 1. core/

core/ 存放具体分析能力。

当前包括：

- file_loader.py：文件读取
- field_detector.py：字段识别
- basic_analysis.py：基础统计
- chart_generator.py：自动图表
- chart_recommender.py：图表推荐
- anomaly_detector.py：异常值检测
- correlation_analysis.py：相关性分析
- cleaning_advisor.py：数据清洗建议

如果以后新增具体分析能力，例如文本关键词分析，应优先放在 core/ 中。

示例：

```text
core/text_analysis.py
```

---

### 2. pipeline/

pipeline/ 负责组织分析流程。

当前包括：

- analysis_pipeline.py
- report_context.py

其中：

- analysis_pipeline.py 负责统一生成所有分析结果
- report_context.py 负责构建 AI 报告需要的统计摘要

后续新增分析功能时，通常需要在 analysis_pipeline.py 中接入。

---

### 3. sections/

sections/ 负责页面展示。

当前包括：

- sidebar_section.py
- home_section.py
- upload_section.py
- workspace_section.py
- overview_section.py
- insight_section.py
- data_detail_section.py
- quality_section.py
- chart_section.py
- report_section.py

如果以后要修改页面样式或布局，应优先修改 sections/ 中对应文件，而不是修改 app.py。

例如：

- 修改左侧边栏：sections/sidebar_section.py
- 修改首页：sections/home_section.py
- 修改上传区域：sections/upload_section.py
- 修改工作台布局：sections/workspace_section.py
- 修改 AI 报告区域：sections/report_section.py

---

### 4. prompts/

prompts/ 存放 AI 提示词。

当前包括：

- general_report_prompt.txt

后续如果新增场景化报告，可以新增：

- survey_report_prompt.txt
- business_report_prompt.txt
- expense_report_prompt.txt

---

### 5. utils/

utils/ 存放通用工具。

当前包括：

- deepseek_client.py

后续如果新增缓存、导出、格式转换，可以放在：

- cache.py
- export.py
- formatters.py

---

## 三、新增功能的标准流程

新增功能时，不要直接改 app.py。

标准流程如下。

### 示例：新增文本关键词分析

第一步：新增 core 模块。

```text
core/text_analysis.py
```

第二步：接入 pipeline。

在 analysis_pipeline.py 中调用文本分析函数，并把结果加入 analysis_result。

第三步：新增或修改 section。

如果需要单独展示，可以新增：

```text
sections/text_section.py
```

如果只是已有页面的一部分，可以放入已有 section。

第四步：如需进入 AI 报告，修改 report_context.py。

第五步：如需 AI 专门解释新结果，修改 prompts/ 中的提示词。

---

## 四、app.py 修改原则

只有以下情况才修改 app.py：

1. 新增全局入口
2. 修改主流程
3. 替换整体页面架构
4. 接入新的顶层分析模式

一般功能增加，不应该直接修改 app.py。

---

## 五、analysis_result 设计规则

analysis_result 是整个项目的数据中枢。

当前结构包括：

```python
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
```

后续新增功能时，应继续把分析结果加入该字典。

命名规则：

- 使用英文 key
- 语义清楚
- 不使用临时变量名
- 不覆盖已有 key

示例：

```python
"text_summary": text_summary
"survey_summary": survey_summary
"business_metrics": business_metrics
```

---

## 六、AI 报告规则

AI 报告不能直接读取完整原始数据。

原因：

1. 降低 API 成本
2. 降低隐私风险
3. 减少 token 消耗
4. 避免长表格导致模型混乱

AI 报告应读取：

- 统计摘要
- 字段结构
- 异常检测结果
- 相关性结果
- 图表推荐
- 清洗建议

这些内容由 pipeline/report_context.py 统一生成。

---

## 七、开发优先级

当前阶段优先级：

1. 结构稳定
2. 页面清晰
3. 功能可维护
4. 输出准确
5. 再考虑美观
6. 最后考虑复杂功能

不要在结构不稳定时盲目增加功能。

---

## 八、版本规划

### v0.6

目标：

- 重构 app.py
- 拆分 pipeline
- 拆分 sections
- 优化工作台界面
- 完成基础项目规范

### v1.0

目标：

- 稳定公开测试版
- 增加示例数据
- 增加复制报告
- 增加错误提示
- 增加隐私提醒
- 优化部署方式

当前状态：

- 已完成基础公开测试能力
- 已兼容本地 .env 和 Streamlit Secrets
- 后续新增功能应优先进入 v2.0 场景化分析，不建议继续扩大 v1.0 范围

### v2.0

目标：

- 问卷数据分析
- 小微商家经营分析
- 个人消费分析
- 数据分析学习陪练

### v3.0

目标：

- 登录系统
- 历史记录
- 项目管理
- 自然语言问数
- 报告导出

### v4.0

目标：

- 多智能体协作
- 自动分析计划
- 审核校验智能体
- 自动周报
- 数据看板
