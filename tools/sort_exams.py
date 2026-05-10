"""각 과목 데이터의 exam을 중복 제거하고 시험일자(exam_date) 내림차순으로 정렬.
유효 날짜(YYYY-MM-DD) 우선, 잘못된 날짜는 뒤로.
2026-sn 등 알려진 수능 날짜는 자동 보정.
"""
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')

# 알려진 수능 시행일 (학년도 → 실시일)
SUNEUNG_DATES = {
    '2023-sn': '2022-11-17',
    '2024-sn': '2023-11-16',
    '2025-sn': '2024-11-14',
    '2026-sn': '2025-11-13',
}

def is_valid_date(s):
    return bool(s and DATE_RE.match(str(s)))

def fix_date(e):
    """알려진 수능 날짜로 보정."""
    if e['exam_id'] in SUNEUNG_DATES:
        e['exam_date'] = SUNEUNG_DATES[e['exam_id']]
    return e

def merge_exam(a, b):
    out = dict(a)
    for k in ['question_pdf_id', 'answer_pdf_id', 'question_pdf_path', 'answer_pdf_path']:
        if not out.get(k) and b.get(k):
            out[k] = b[k]
    if not is_valid_date(out.get('exam_date')) and is_valid_date(b.get('exam_date')):
        out['exam_date'] = b['exam_date']
    return out

def dedup_and_sort(exams):
    by_id = {}
    for e in exams:
        e = fix_date(e)
        eid = e['exam_id']
        if eid not in by_id:
            by_id[eid] = e
        else:
            existing = by_id[eid]
            if is_valid_date(e.get('exam_date')) and not is_valid_date(existing.get('exam_date')):
                by_id[eid] = merge_exam(e, existing)
            else:
                by_id[eid] = merge_exam(existing, e)

    def sort_key(e):
        d = e.get('exam_date', '')
        return d if is_valid_date(d) else ''

    return sorted(by_id.values(), key=sort_key, reverse=True)

for sub in ['korean', 'math', 'english']:
    for path_rel in [f'data/{sub}.json', f'tools/ad_{sub}_init.json']:
        path = os.path.join(ROOT, path_rel)
        if not os.path.exists(path):
            continue
        # BOM 대응
        with open(path, encoding='utf-8-sig') as f:
            data = json.load(f)
        before = len(data['exams'])
        data['exams'] = dedup_and_sort(data['exams'])
        after = len(data['exams'])
        # BOM 없이 저장
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'{path_rel}: {before} -> {after}')
        for e in data['exams']:
            print(f'  {e["exam_id"]:10s} | {e.get("exam_date","-"):12s} | {e["exam_name"]}')
        print()
