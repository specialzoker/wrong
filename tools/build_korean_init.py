"""data/korean.json → tools/ad_korean_init.json 변환
exam_id의 Date 문자열을 짧은 ID로 정규화하고 불필요한 필드 제거.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).parent.parent

ID_MAP = {
    "Sat Jun 01 2024 00:00:00 GMT+0900 (Korean Standard Time)": "2024-6",
    "Sun Sep 01 2024 00:00:00 GMT+0900 (Korean Standard Time)": "2024-9",
    "Sun Jun 01 2025 00:00:00 GMT+0900 (Korean Standard Time)": "2025-6",
    "Mon Sep 01 2025 00:00:00 GMT+0900 (Korean Standard Time)": "2025-9",
    "Sun Mar 01 2026 00:00:00 GMT+0900 (Korean Standard Time)": "2026-3",
}

DATE_MAP = {
    "2023-sn": "2022-11-17",
    "2024-6":  "2024-06-04",
    "2024-9":  "2024-09-04",
    "2024-sn": "2023-11-16",
    "2025-6":  "2025-06-03",
    "2025-9":  "2025-09-03",
    "2025-sn": "2024-11-14",
    "2026-sn": "2025-11-13",
    "2026-3":  "2026-03-26",
}

src = ROOT / "data" / "korean.json"
dst = ROOT / "tools" / "ad_korean_init.json"

with open(src, encoding="utf-8") as f:
    data = json.load(f)

# 시험 정규화
for exam in data.get("exams", []):
    exam["exam_id"] = ID_MAP.get(exam["exam_id"], exam["exam_id"])
    exam["exam_date"] = DATE_MAP.get(exam["exam_id"], "")
    for k in ["subject", "total_questions"]:
        exam.pop(k, None)

# 문항 exam_id 정규화
for q in data.get("questions", []):
    q["exam_id"] = ID_MAP.get(q["exam_id"], q["exam_id"])

exams = data.get("exams", [])
questions = data.get("questions", [])
print(f"시험 {len(exams)}개, 문항 {len(questions)}개 → {dst}")

with open(dst, "w", encoding="utf-8") as f:
    json.dump({"exams": exams, "questions": questions}, f, ensure_ascii=False, indent=2)

print("완료!")
