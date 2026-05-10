import json, openpyxl

wb = openpyxl.load_workbook(r'C:\Users\user\Downloads\수학.xlsx', data_only=True)

# exam_id 정규화 맵
idMap = {
    '2025-suneung': '2026-sn',
    '2024-suneung': '2025-sn',
    '2023-suneung': '2024-sn',
    '2025-09': '2025-9', '2025-06': '2025-6',
    '2024-09': '2024-9', '2024-06': '2024-6',
    '2023-09': '2023-9', '2023-06': '2023-6',
    '2026-03': '2026-3',
}
nameMap = {
    '2026-sn': '2026학년도 수능', '2025-sn': '2025학년도 수능',
    '2024-sn': '2024학년도 수능', '2023-sn': '2023학년도 수능',
    '2025-9': '2025년 9월 모의고사', '2025-6': '2025년 6월 모의고사',
    '2024-9': '2024년 9월 모의고사', '2024-6': '2024년 6월 모의고사',
    '2023-9': '2023년 9월 모의고사', '2023-6': '2023년 6월 모의고사',
    '2026-3': '2026년 3월 모의고사',
}

# ── 모의고사목록 ──
ws1 = wb['모의고사목록']
exams = []
seen_exams = set()
for r in range(2, ws1.max_row + 1):
    raw_id = str(ws1.cell(r, 1).value or '').strip()
    if not raw_id:
        continue
    # 날짜 형식 exam_id 처리 (예: 2026-03-01 00:00:00)
    if raw_id.startswith('2026-03'):
        raw_id = '2026-03'
    eid = idMap.get(raw_id, raw_id)
    if eid in seen_exams:
        continue
    seen_exams.add(eid)

    date_val = ws1.cell(r, 4).value
    if hasattr(date_val, 'strftime'):
        exam_date = date_val.strftime('%Y-%m-%d')
    else:
        exam_date = str(date_val or '').strip()[:10]

    q_id = str(ws1.cell(r, 7).value or '').strip()
    a_id = str(ws1.cell(r, 9).value or '').strip()

    e = {
        'exam_id': eid,
        'exam_name': nameMap.get(eid, eid),
        'subject': '수학',
        'exam_date': exam_date,
        'total_questions': 30,
    }
    if q_id and len(q_id) > 10:
        e['question_pdf_id'] = q_id
    if a_id and len(a_id) > 10:
        e['answer_pdf_id'] = a_id
    exams.append(e)

# 2023-sn 없으면 추가
if not any(e['exam_id'] == '2023-sn' for e in exams):
    exams.append({'exam_id': '2023-sn', 'exam_name': '2023학년도 수능', 'subject': '수학', 'exam_date': '2022-11-17', 'total_questions': 30})

# exam_id 순서 정렬
order = ['2026-sn','2025-sn','2024-sn','2023-sn','2025-9','2025-6','2024-9','2024-6','2026-3','2023-9','2023-6']
exams.sort(key=lambda e: order.index(e['exam_id']) if e['exam_id'] in order else 99)

# ── 문항정보 ──
ws2 = wb['문항정보']
questions = []
seen_q = set()
ans_map = {'①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5'}

for r in range(2, ws2.max_row + 1):
    raw_id = str(ws2.cell(r, 1).value or '').strip()
    if not raw_id:
        continue
    eid = idMap.get(raw_id, raw_id)
    qno = ws2.cell(r, 2).value
    if qno is None:
        continue
    qno = int(qno)
    ic = str(ws2.cell(r, 11).value or '').strip()

    key = f'{eid}|{qno}|{ic}'
    if key in seen_q:
        continue
    seen_q.add(key)

    ans_raw = str(ws2.cell(r, 9).value or '').strip()
    ans = ans_map.get(ans_raw, ans_raw)

    qp = ws2.cell(r, 7).value
    ap = ws2.cell(r, 8).value
    sc = ws2.cell(r, 10).value

    questions.append({
        'exam_id': eid,
        'question_no': qno,
        'is_common': ic,
        'topic': str(ws2.cell(r, 3).value or '').strip(),
        'subtopic': str(ws2.cell(r, 4).value or '').strip(),
        'difficulty': str(ws2.cell(r, 5).value or '').strip(),
        'keywords': str(ws2.cell(r, 6).value or '').strip(),
        'question_page': int(qp) if qp else 1,
        'answer_page': int(ap) if ap else 1,
        'correct_answer': ans,
        'score': int(sc) if sc else 2,
    })

result = {'exams': exams, 'questions': questions}
with open(r'C:\Users\user\wrong\tools\ad_math_init.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f'완료! 시험 {len(exams)}개, 문항 {len(questions)}개')
by_id = {}
for q in questions:
    by_id[q['exam_id']] = by_id.get(q['exam_id'], 0) + 1
for k in order:
    if k in by_id:
        print(f'  {k}: {by_id[k]}문항')
for e in exams:
    qcnt = by_id.get(e['exam_id'], 0)
    has_q = '문제O' if e.get('question_pdf_id') else '문제X'
    has_a = '정답O' if e.get('answer_pdf_id') else '정답X'
    print(f'  {e["exam_id"]:10s} {e["exam_name"]} | {has_q} | {has_a} | {qcnt}문항')
