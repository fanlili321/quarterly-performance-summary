#!/usr/bin/env python3
"""Fill Fan Lili-style quarterly appraisal workbooks."""

from __future__ import annotations

import argparse
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Alignment


ROWS = {
    "work_output": 4,
    "ai_application": 5,
    "comprehensive": 6,
}


def chinese_len(text: str) -> int:
    return len(text or "")


def parse_grades(raw: str) -> list[str]:
    grades = [item.strip() for item in raw.split(",") if item.strip()]
    if len(grades) != 3:
        raise ValueError("--grades must contain exactly three comma-separated values, e.g. A,A,A")
    return grades


def main() -> None:
    parser = argparse.ArgumentParser(description="Fill quarterly self-review rows in an Excel workbook.")
    parser.add_argument("--input", required=True, help="Input .xlsx appraisal template.")
    parser.add_argument("--output", required=True, help="Output .xlsx path.")
    parser.add_argument("--work-output", required=True, help="Description for row 4 / work output.")
    parser.add_argument("--ai-application", required=True, help="Description for row 5 / AI application.")
    parser.add_argument("--comprehensive", required=True, help="Description for row 6 / comprehensive capability.")
    parser.add_argument("--grades", default="A,A,A", help="Three comma-separated grades for rows 4-6.")
    parser.add_argument("--sheet", default=None, help="Optional worksheet name. Defaults to active sheet.")
    parser.add_argument("--max-chars", type=int, default=200, help="Warn when a description exceeds this many chars.")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser()
    output_path = Path(args.output).expanduser()
    if not input_path.exists():
        raise FileNotFoundError(input_path)

    grades = parse_grades(args.grades)
    texts = {
        "work_output": args.work_output,
        "ai_application": args.ai_application,
        "comprehensive": args.comprehensive,
    }

    for name, text in texts.items():
        length = chinese_len(text)
        if length > args.max_chars:
            print(f"[WARN] {name} is {length} chars, over --max-chars={args.max_chars}")

    workbook = load_workbook(input_path)
    worksheet = workbook[args.sheet] if args.sheet else workbook.active

    for index, (key, row) in enumerate(ROWS.items()):
        grade_cell = worksheet[f"C{row}"]
        text_cell = worksheet[f"E{row}"]
        grade_cell.value = grades[index]
        text_cell.value = texts[key]
        grade_cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        text_cell.alignment = Alignment(vertical="top", wrap_text=True)
        worksheet.row_dimensions[row].height = max(80, worksheet.row_dimensions[row].height or 0)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(output_path)
    print(f"[OK] wrote {output_path}")
    for key, text in texts.items():
        print(f"{key}: {chinese_len(text)} chars")


if __name__ == "__main__":
    main()
