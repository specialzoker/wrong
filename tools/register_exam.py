"""
시험 자동 등록 도구 — Claude 분류 스킬이 만든 JSON을 data/*.json에 바로 넣는다.
(어드민의 'JSON 붙여넣기 → 적용'과 같은 규칙. 세분화 필드 unit·code·tags 등도 보존)

  등록/갱신:  python3 tools/register_exam.py register --subject math --exam-id 2026_10 \
                 --name "2026년 10월 모의고사" --date 2026-10-20 --cls classification/math_classification_26_10.json
              문제 PDF(pdfs/{exam_id}_{과목}_q.pdf)가 있으면 문항별 페이지를 자동으로 찾는다.
  페이지 점검: python3 tools/register_exam.py fix-pages [--subject math] [--dry]
"""
import argparse, json, os, re, subprocess, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABEL = {'korean': '국어', 'math': '수학', 'english': '영어'}
FKEY = {'korean': 'is_common', 'math': 'is_common', 'english': 'section'}
TOTAL = {'korean': 45, 'math': 30, 'english': 45}
ALIAS = {
    'common': ['common', '공통'], 'hwajak': ['hwajak', '화작', '화법과작문', '화법'],
    'eonmae': ['eonmae', '언매', '언어와매체', '언어', '매체'],
    'hwaktong': ['hwaktong', 'hwaktonge', 'hwakt', '확통', '확률과통계', '확률과 통계', '선택-확통'],
    'mijeok': ['mijeok', 'mijeokbun', 'mijeokbu', '미적분', '선택-미적분'],
    'giha': ['giha', '기하', '선택-기하'], 'listening': ['listening', '듣기'], 'reading': ['reading', '독해'],
}
SEC_TO_VAL = {'common': '공통', 'hwajak': '화법과작문', 'eonmae': '언어와매체', 'hwaktong': '선택-확통',
              'mijeok': '선택-미적분', 'giha': '선택-기하', 'listening': '듣기', 'reading': '독해'}
SKIP = {'q', 'section', 'answer', 'answer_value', 'correct_answer', 'exam_id', 'question_no', 'is_common',
        'question_page', 'answer_page', 'difficulty', 'topic', 'subtopic', 'score', 'keywords'}
CIRCLE = {'①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5'}
PDF_SEC = {'확률과 통계': '선택-확통', '미적분': '선택-미적분', '기하': '선택-기하',
           '화법과 작문': '화법과작문', '언어와 매체': '언어와매체'}

def sec_val(s):
    s = str(s or '').strip().lower()
    for k, names in ALIAS.items():
        if s in [n.lower() for n in names]: return SEC_TO_VAL[k]
    raise ValueError(f'알 수 없는 section: {s}')

def page_map(pdf):
    """PDF 각 페이지에서 문항 번호를 찾아 {(선택과목|None, 번호): 페이지}"""
    info = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    n = int(re.search(r'Pages:\s+(\d+)', info).group(1))
    out = {}
    for p in range(1, n + 1):
        t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), '-layout', pdf, '-'],
                           capture_output=True, text=True).stdout
        sec = next((v for k, v in PDF_SEC.items() if '(' + k + ')' in t[:600]), None)
        for m in re.finditer(r'(?:^|\s{2,})(\d{1,2})\.\s', t, re.M):
            out.setdefault((sec, int(m.group(1))), p)
    return out

def page_of(pages, val, no):
    key = (None if val in ('공통', '듣기', '독해') else val, no)
    return pages.get(key) or pages.get((None, no))

def now(): return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

def load(sub):
    return json.load(open(os.path.join(ROOT, 'data', sub + '.json'), encoding='utf-8'))

def dump(sub, data):
    data['updated_at'] = now()   # 어드민이 열릴 때 이 값으로 최신 여부를 판단
    data['exams'] = sorted(data['exams'], key=lambda e: e.get('exam_date', '') if re.match(r'^\d{4}-\d{2}-\d{2}$', str(e.get('exam_date', ''))) else '', reverse=True)
    with open(os.path.join(ROOT, 'data', sub + '.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def register(a):
    sub, eid = a.subject, a.exam_id
    data, fkey = load(sub), FKEY[sub]
    qpdf = a.qpdf or f'pdfs/{eid}_{LABEL[sub]}_q.pdf'
    apdf = a.apdf or f'pdfs/{eid}_{LABEL[sub]}_a.pdf'
    has_q, has_a = os.path.exists(os.path.join(ROOT, qpdf)), os.path.exists(os.path.join(ROOT, apdf))

    exam = next((e for e in data['exams'] if e['exam_id'] == eid), None)
    if not exam:
        if not (a.name and a.date): sys.exit('새 시험은 --name, --date가 필요합니다')
        exam = {'exam_id': eid, 'exam_name': a.name}
        if any('subject' in e for e in data['exams']): exam['subject'] = LABEL[sub]
        exam.update(exam_date=a.date, total_questions=TOTAL[sub])
        data['exams'].append(exam); print('시험 추가:', eid)
    else:
        if a.name: exam['exam_name'] = a.name
        if a.date: exam['exam_date'] = a.date
        print('기존 시험 갱신:', eid)
    if has_q: exam['question_pdf_path'] = qpdf
    if has_a: exam['answer_pdf_path'] = apdf

    pages = page_map(os.path.join(ROOT, qpdf)) if has_q else {}
    items = json.load(open(os.path.join(ROOT, a.cls) if not os.path.isabs(a.cls) else a.cls, encoding='utf-8'))
    created = updated = 0
    for it in items:
        no, val = int(it['q']), sec_val(it['section'])
        ans = str(it['answer_value']) if 'answer_value' in it else CIRCLE.get(str(it.get('answer', '')), str(it.get('answer', '')))
        pg = page_of(pages, val, no)
        q = next((x for x in data['questions'] if x['exam_id'] == eid and x['question_no'] == no and x.get(fkey) == val), None)
        if q is None:
            q = {'exam_id': eid, 'question_no': no, 'topic': it.get('topic', ''), 'subtopic': it.get('subtopic', ''),
                 'difficulty': '상' if '고난도' in (it.get('tags') or []) else '중', 'keywords': it.get('keywords', ''),
                 'question_page': pg or 1, 'answer_page': 1, 'correct_answer': ans, 'score': it.get('score', 2), fkey: val}
            data['questions'].append(q); created += 1
        else:
            if q.get('correct_answer') not in (None, '', ans) and not a.force_answer:
                print(f'  ⚠ {val} {no}번 정답이 다름: 기존 {q["correct_answer"]} / 새 {ans} → 기존 값 유지 (--force-answer로 덮어쓰기)')
            else:
                q['correct_answer'] = ans
            for k in ('topic', 'subtopic', 'score', 'keywords'):
                if k in it: q[k] = it[k]
            if pg: q['question_page'] = pg
            updated += 1
        for k, v in it.items():
            if k not in SKIP: q[k] = v
        if has_q and not pg: print(f'  ⚠ {val} {no}번 페이지를 PDF에서 찾지 못함')
    dump(sub, data)
    print(f'완료: 신규 {created}문항, 갱신 {updated}문항 / 문제PDF {"O" if has_q else "X"} 정답파일 {"O" if has_a else "X"}')

def fix_pages(a):
    for sub in ([a.subject] if a.subject else ['korean', 'math', 'english']):
        data, fkey, changed = load(sub), FKEY[sub], 0
        for e in data['exams']:
            p = e.get('question_pdf_path')
            if not p or not os.path.exists(os.path.join(ROOT, p)): continue
            pages, n = page_map(os.path.join(ROOT, p)), 0
            for q in data['questions']:
                if q['exam_id'] != e['exam_id']: continue
                pg = page_of(pages, q.get(fkey), q['question_no'])
                if pg and pg != q.get('question_page'):
                    if not a.dry: q['question_page'] = pg
                    n += 1
            if n: print(f'{LABEL[sub]} {e["exam_id"]}: 페이지 {n}개 {"틀림" if a.dry else "수정"}')
            changed += n
        if changed and not a.dry: dump(sub, data)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
    r = sp.add_parser('register')
    r.add_argument('--subject', required=True, choices=list(LABEL)); r.add_argument('--exam-id', required=True)
    r.add_argument('--cls', required=True); r.add_argument('--name'); r.add_argument('--date')
    r.add_argument('--qpdf'); r.add_argument('--apdf'); r.add_argument('--force-answer', action='store_true')
    f = sp.add_parser('fix-pages'); f.add_argument('--subject', choices=list(LABEL)); f.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    register(a) if a.cmd == 'register' else fix_pages(a)
