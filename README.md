# Data 合规星 · 隐私政策智能审查工作流

**English:** Agentic workflow on Tencent Cloud for **privacy-policy review and compliance report generation** — prompts, orchestration export, and Python glue code for document handling and COS URLs.

---

## 面试官快速了解（30 秒版）

| 维度 | 内容 |
|------|------|
| **要解决什么** | 把「隐私政策合规审查」从一次性咨询，变成可重复执行的标准化智能体流程：收文档 → 解析分块 → 多阶段大模型审查/修订 → 生成评估类输出 → 导出可分享的 Markdown/Word 链路。 |
| **平台形态** | 腾讯云智能体开发平台工作流（已导出 JSON，可导入复盘结构）。 |
| **你能直接看的东西** | 工作流 JSON、多段 **System/User 提示词**（`.txt`）、文件解析与 URL 处理的 **Python 节点代码**。 |
| **产品向亮点** | 场景选在 **数据合规 / 企业法务** 高价值 B 端；流程拆成多节点，便于迭代提示词与风控；工程上 **密钥不进仓库**（环境变量）。 |

> 建议在简历/GitHub 简介里用一句话：**基于腾讯云智能体平台搭建隐私政策审查多节点工作流，负责需求拆解、提示词设计与流程导出，并协同代码节点完成文档解析与对象存储交付。**

---

## 仓库里有什么（结构）

```
├── README.md                          # 本说明（面向展示与复现）
├── 文件说明.txt                       # 原始文件索引（导出说明）
├── requirements.txt                   # Python 依赖
├── .env.example                       # COS 等环境变量示例（勿提交真实密钥）
│
├── 工作流1.png ~ 工作流3.png          # 画布/流程截图（便于一眼看懂拓扑）
├── 文件收集节点输出变量.png
├── md2word插件输出变量.png
│
├── 隐私政策审查与修订1.txt            # 大模型提示词（审查/修订相关）
├── 隐私政策审查与修订2.txt
├── 生成评估报告.txt                  # 评估报告类提示词
│
├── text.py                            # 文档提取与按章节分块（对接文件收集节点）
├── word_url.py                        # 从插件输出中解析 Word 下载 URL
├── md_url.py / md_url2.py             # Markdown 合并或单段上传 COS，返回可访问 URL
│
└── export-Data合规星-…/               # 平台导出包
    ├── c5b873df-…_workflow.json       # 工作流定义（可导入平台）
    ├── 工作流程.xlsx / 变量.xlsx 等   # 平台导出的表格说明
    └── …
```

---

## 产品与流程（文字版架构）

1. **输入**：用户上传隐私政策文档（及自然语言意图）。  
2. **预处理**：`text.py` 侧提取正文、按约定关键词拆分段落，便于分阶段审查。  
3. **核心智能**：多节点 LLM 调用，提示词见各 `.txt`（可按岗位侧重讲：边界条件、输出格式、合规要点覆盖）。  
4. **交付**：通过 `md_url` / `md_url2` 将 Markdown 落到对象存储并回传 URL；`word_url` 解析 Word 插件返回链路。  

截图与 JSON 对照阅读，便于在面试中 **边讲边指**。

---

## 本地复现（代码节点）

```bash
cd /path/to/this/repo
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # 填入你自己的腾讯云 COS 密钥（请先在控制台轮换、禁用旧密钥）
# 按需运行：python text.py / python md_url.py 等
```

导入工作流：在腾讯云智能体平台使用 `export-…/c5b873df-…_workflow.json`；若代码节点需配置环境变量，请在控制台为 **SecretId/SecretKey** 配置密钥管理，**不要**写回 JSON 再提交到公开仓库。

---

## 安全与合规说明

- 仓库内 **不包含** 真实 API/COS 密钥；历史若曾泄露密钥，请务必在云平台 **轮换密钥**。  
- 面试演示建议使用 **脱敏样例文档**，避免上传真实用户隐私政策全文到公开议题。

---

## 建议在 GitHub 上再做的两步（界面层）

1. **仓库命名**：优先英文短名，便于搜索与写在简历上，例如 `privacy-policy-compliance-agent`、`data-heguixing-workflow`。  
2. **Topics 标签**：例如 `agent`, `llm`, `workflow`, `privacy`, `compliance`, `tencent-cloud`, `prompt-engineering`（按实际技术栈勾选）。

---

## 个人贡献（请按需改写）

以下占位请替换为你的真实分工，避免简历与仓库不一致：

- [ ] 需求与场景定义、竞品/法规要点梳理  
- [ ] 工作流节点拆分与 PRD 级逻辑说明  
- [ ] 提示词撰写与多轮评测记录  
- [ ] 与研发联调：文件节点、COS、插件输出字段对齐  

---

## License

MIT License — 若赛事主办方或所在单位对代码开源有限制，请删除或替换本文件并同步更新本说明。
