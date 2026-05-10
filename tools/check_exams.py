import json
for sub in ['korean', 'math', 'english']:
    with open(f'data/{sub}.json', encoding='utf-8') as f:
        d = json.load(f)
    print(f'=== {sub} ({len(d["exams"])} exams) ===')
    for e in d['exams']:
        eid = e['exam_id']
        edate = e.get('exam_date', '-')
        ename = e['exam_name']
        print(f'  {eid:10s} | {edate:12s} | {ename}')
