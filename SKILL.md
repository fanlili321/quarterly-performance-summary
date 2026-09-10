---
name: quarterly-performance-summary
description: Create Chinese quarterly work summaries and performance self-review drafts for 范丽丽 / 银行螺丝钉 content work, including evidence collection from Feishu sheets, docs, group chats, Drive folders, live-course exports, and local Excel appraisal forms. Use when the user asks for 季度总结、Q1/Q2/Q3/Q4工作总结、绩效自评、考核表填写、年度总结与考核、自评等级说明、工作产出/AI应用/团队协作/需提升总结.
---

# Quarterly Performance Summary

## Core Workflow

Use this skill to turn quarterly evidence into a concrete Chinese self-review and, when requested, fill the appraisal Excel.

1. Confirm the year and quarter. If absent, infer from the user's files or current date, but ask before writing final appraisal text when the quarter is ambiguous.
2. Collect evidence from the relevant sources:
   - Work-record sheet. Default known sheet: `https://epndqwwg0a.feishu.cn/sheets/shtcnqIGHAXSAxYPpjtQ7Tic4eC?sheet=JPDrk2`. Read the month tabs matching the quarter, not only the tab included in the URL.
   - Feishu group chats. Search `226课程群`, PPT制作相关群, `内容&渠道组`, `内容小分队`, `富豪榜前`, `文章小组`; resolve exact chat names if search returns variants.
   - External livestream/offline activity Drive folder. Default folder: `https://epndqwwg0a.feishu.cn/drive/folder/DU88fYBMblNlNmdah5lcHpl8nAc`. Always use this folder when the user mentions 对外直播 or 线下活动 unless the user gives a different folder.
   - Local/export files supplied by the user, such as live-list CSVs and appraisal `.xlsx` templates.
3. Build an evidence table with four buckets: 工作产出, AI应用, 团队协作/综合能力, 需要提升.
4. Run the mandatory missed-item audit before drafting or filling:
   - Compare final bullets against the work-record sheet, chat evidence, and Drive file counts.
   - Specifically check AI-related items, 图片素材库, 对外直播/线下活动 PPTs, 高净值/富豪相关工作, 文章/图书/出版社协作, data-check or复核 work.
   - Remove any item whose owner is not confirmed as the user. If ownership is unclear, mark it as "协同/参与" or ask.
5. Draft concise, concrete appraisal language. Prefer exact counts, issue names, project names, and impact over broad adjectives.
6. If filling Excel, use `scripts/fill_self_review.py` after preparing final text and grades.

## Tool And Skill Routing

When actually reading or modifying Feishu resources, first load the matching Lark skill:

- Feishu docs/wiki/docx: use `lark-doc` or `lark-wiki` as appropriate.
- Feishu sheets: use `lark-sheets`.
- Feishu Drive folders/files: use `lark-drive`.
- Feishu group chat search: use `lark-im`.
- Local `.xlsx` files: use the spreadsheet skill when analysis or editing is non-trivial.

Prefer official Lark CLI operations where available. Quote URLs containing `?` in shell commands.

## Evidence Rules

For the external/offline activity folder, count source presentation files by dated activity:

- Include Keynote, PPT, and PPTX source decks that fall within the quarter.
- Exclude PDF/JPEG/image exports when a source deck exists.
- Deduplicate the same date/title when both `.key` and `.pptx` versions represent the same event.
- Use file names with dates as evidence; if dates conflict, inspect file metadata or ask.

For live-course exports:

- Filter by the quarter date range.
- Exclude obvious test sessions.
- Report session count, views, viewers, new users, replay metrics, and strong themes when available.

For chat evidence:

- Prioritize messages sent by 范丽丽 and direct @mentions to her.
- Search with quarter dates and keywords such as `AI`, `PPT`, `大纲`, `直播`, `线下`, `高净值`, `富豪榜前`, `财富脑图`, `复核`, `图片素材库`, `skill`, `自动化`, `数据异常`, `GitHub`, `gitehub`.
- Do not paste raw chat excerpts into the appraisal unless the user asks; summarize evidence into work facts.

## Writing Guidance

Read `references/writing-guide.md` before finalizing appraisal text.

For an A self-rating, the text must prove scope and initiative:

- State concrete outputs: number of sessions, PPTs, documents, projects, or workflows.
- Name representative examples and responsible role.
- Include thinking: what bottleneck was found, what process was improved, what risk was reduced.
- Include AI improvement only when it belongs to the user or was clearly driven by the user.
- Include a short "需提升" point when the form asks for reflection, but do not let it weaken the grade.

Avoid vague wording such as "认真负责、积极配合、提升效率" unless attached to a concrete example.

## Filling Excel

Use `scripts/fill_self_review.py` for appraisal workbooks where rows 4-6 are:

- Row 4: 工作产出
- Row 5: 职业能力/AI应用
- Row 6: 职业能力/综合

The script writes grades to column C and descriptions to column E, preserves the original workbook, wraps text, and saves a copy.

Example:

```bash
python3 scripts/fill_self_review.py \
  --input "/path/to/2026Q2绩效自评表.xlsx" \
  --output "/path/to/2026Q2绩效自评表（范丽丽-已填写）.xlsx" \
  --work-output "Q2完成..." \
  --ai-application "Q2 AI从..." \
  --comprehensive "Q2承担..." \
  --grades A,A,A
```

If the form states a character limit, keep each description within that limit and verify after writing.
