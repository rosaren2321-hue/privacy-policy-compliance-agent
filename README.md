# Data 合规星 — 隐私政策智能审查 Agent

> Privacy-policy compliance review agent built on Tencent Cloud ADP (Agent Development Platform).
> Upload an app privacy policy → get a revised draft with tracked changes + a PII compliance assessment report.

---

## Problem

China's regulators have shifted from "formal check" to "substantive review" of app privacy policies. Manual review is **expensive, slow, and inconsistent**; generic LLMs hallucinate legal citations; pure rule-based tools can't produce **actionable legal text**.

**Data 合规星** bridges this gap: it combines regulation knowledge, industry templates for **39 app categories**, and structured prompt chains to deliver **reviewable, editable compliance documents** — not just a checklist.

---

## What It Does — "一体两翼" (One Core, Two Wings)

| Module | Description |
|--------|-------------|
| **Core: Policy Review & Revision** | Parses uploaded `.docx` → splits by chapter → runs two-stage LLM review (Part 1: chapters 1-3, Part 2: chapters 4-10) → outputs revised policy with ~~strikethrough~~ / **bold** / <font color="red">red additions</font> markup |
| **Wing 1: PII Compliance Assessment** | Cross-validates policy text + 15-question survey → risk rating (High / Medium / Low) per category → structured assessment report (9×32 indicator framework) |
| **Wing 2: Legal Q&A** | RAG-powered consultation on data compliance regulations and enforcement cases |

This repo covers the **Core** and the report generation pipeline.

---

## Workflow Architecture

The entire agent runs as a **multi-node workflow** on Tencent Cloud ADP (similar to Coze / Dify). No standalone backend — the platform handles orchestration, model calls, and plugin execution.

```
┌─────────────┐     ┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  User Input  │────▶│  File Parse   │────▶│  LLM Review ×2   │────▶│  Merge & COS  │
│  (.docx)     │     │  (docx_parser)│     │  (prompt chains) │     │  Upload       │
└─────────────┘     └──────────────┘     └──────────────────┘     └──────────────┘
                                                                          │
                                                                          ▼
                                                                   Download URL
                                                                   (Markdown / Word)
```

---

## Key Design Decisions

| Decision | Why |
|----------|-----|
| **Temperature 0.2 / Top-P 0.3** | Legal text demands precision over creativity; low randomness reduces hallucination of non-existent regulations |
| **Two-stage prompt split (Part 1 + Part 2)** | A single prompt for all 10 chapters exceeded context limits and degraded output quality; splitting by chapter groups keeps each prompt focused |
| **Tracked-changes markup** (strikethrough + bold + red) | Lawyers need to see *what changed and why* — a clean rewrite without markup is unusable in legal review workflows |
| **Template-driven revision with data carry-over** | Standard clauses come from a curated template library; business-specific data (SDK lists, contact info, data fields) is extracted and preserved verbatim from the original policy |
| **COS upload for delivery** | The platform doesn't natively support file downloads; uploading to Tencent Cloud Object Storage and returning a URL was the pragmatic workaround |

---

## Repo Structure

```
├── README.md
├── workflow/
│   ├── workflow.json              # Full workflow export (importable to ADP)
│   ├── flow-steps.xlsx            # Node-level flow documentation
│   ├── parameters.xlsx            # Parameter configuration
│   ├── variables.xlsx             # Variable definitions
│   ├── flow-references.xlsx       # Cross-node references
│   └── sample-queries.xlsx        # Example user inputs
├── prompts/
│   ├── policy-review-part1.txt    # LLM prompt: chapters 1-3 (modules A-E)
│   ├── policy-review-part2.txt    # LLM prompt: chapters 4-10 (modules F-J)
│   └── assessment-report.txt      # LLM prompt: PII assessment report
├── nodes/                         # Python code nodes (run inside ADP workflow)
│   ├── docx_parser.py             # Extract text from .docx, split by chapter
│   ├── md_merge_upload.py         # Merge markdown outputs → upload to COS
│   ├── md_upload.py               # Single markdown → upload to COS
│   └── word_url_extractor.py      # Extract download URL from plugin response
├── docs/
│   └── product-brief.zh-CN.md     # One-page product brief (sanitized)
├── .env.example
├── requirements.txt
└── LICENSE
```

---

## Prompt Engineering Highlights

The prompts in `prompts/` are the core IP of this project. Key patterns:

- **Role assignment**: Each prompt starts with a specific persona ("隐私政策重构引擎-Part1") with clearly scoped responsibilities
- **Module-based template library**: Clauses are organized into reusable modules (A through J), each covering a specific legal topic with fill-in-the-blank slots
- **Three-tier markup protocol**: The prompt enforces strict formatting rules — strikethrough for corrections, bold for replacements, red for additions — ensuring consistent, review-friendly output
- **Data preservation directive**: Explicit instructions to "carry over" business-specific data verbatim, preventing the LLM from paraphrasing or dropping critical details like SDK names, contact info, and data field lists

---

## How to Import & Run

1. Import `workflow/workflow.json` into Tencent Cloud ADP (or compatible platform)
2. Configure secrets via platform's key management (see `.env.example` for required variables)
3. Upload a `.docx` privacy policy to test

For local testing of individual code nodes:

```bash
pip install -r requirements.txt
cp .env.example .env  # fill in your COS credentials
python nodes/docx_parser.py  # etc.
```

---

## My Role

Team lead for this project. Responsible for:
- Product definition: user personas, pain-point analysis, competitive positioning, the D.A.T.A. design philosophy
- Workflow architecture: node decomposition, data flow between LLM / code / plugin nodes
- Prompt engineering: designed the two-stage review framework, template module library (A-J), and markup protocol
- Code nodes: document parsing, COS upload pipeline, URL extraction logic
- Quality iteration: testing against real privacy policies across multiple app categories

See [`docs/product-brief.zh-CN.md`](docs/product-brief.zh-CN.md) for a one-page product overview.

---

## Security

- No real credentials in this repo — all secrets via environment variables
- Demo materials use anonymized/fictional privacy policies only

## License

MIT
