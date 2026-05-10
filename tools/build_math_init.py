import json, csv

questions = []
idMapQ = {'2025-suneung':'2026-sn','2024-suneung':'2025-sn','2024_수능':'2024-sn'}
seen = set()
with open(r'C:\Users\user\Downloads\[정현석] 수학기출_추천앱_템플릿의 사본 - 문항정보.csv', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        eid = idMapQ.get(row['exam_id'], row['exam_id'])
        qno = int(row['question_no'])
        ic  = row['is_common']
        key = f'{eid}|{qno}|{ic}'
        if key in seen: continue
        seen.add(key)
        ans = row['correct_answer'].replace('①','1').replace('②','2').replace('③','3').replace('④','4').replace('⑤','5')
        questions.append({
            'exam_id': eid, 'question_no': qno, 'is_common': ic,
            'topic': row['topic'], 'subtopic': row['subtopic'], 'difficulty': row['difficulty'],
            'keywords': row['keywords'],
            'question_page': int(row['question_page'] or 1),
            'answer_page': int(row['answer_page'] or 1),
            'correct_answer': ans, 'score': int(row['score'])
        })

exams = [
  {'exam_id':'2026-sn','exam_name':'2026학년도 수능','subject':'수학','exam_date':'2025-11-13','total_questions':30,'question_pdf_id':'1rfCBWY2cy_SKlHUdEihRunfjpLVX4F1u','answer_pdf_id':'15A2xWgGy55wUWSYNNpXGdQ1DE8U1v5Y4'},
  {'exam_id':'2025-sn','exam_name':'2025학년도 수능','subject':'수학','exam_date':'2024-11-14','total_questions':30,'question_pdf_id':'1KsgytqdTC876XDOIdr02V_h9_hQ0TNej','answer_pdf_id':'1UzPLJz8Dx8Q-0DiDDr6o9M72eUSszFF2'},
  {'exam_id':'2024-sn','exam_name':'2024학년도 수능','subject':'수학','exam_date':'2023-11-16','total_questions':30,'question_pdf_id':'1_2PPDeTkJ36gJQRGML8gR4F1Ad_-jms4','answer_pdf_id':'1NzPH2I93NvpOMRvi9V0Rpz_-MAmdrnGY'},
  {'exam_id':'2023-sn','exam_name':'2023학년도 수능','subject':'수학','exam_date':'2022-11-17','total_questions':30},
  {'exam_id':'2025-9','exam_name':'2025년 9월 모의고사','subject':'수학','exam_date':'2025-09-03','total_questions':30,'question_pdf_id':'15-UvkE1tAlQU3iB-rga9qYUYWI4FWRkm','answer_pdf_id':'1l3GtukEZTXNSmrOy250pM_pc93bSVMDv'},
  {'exam_id':'2025-6','exam_name':'2025년 6월 모의고사','subject':'수학','exam_date':'2025-06-04','total_questions':30,'question_pdf_id':'1oyhfXJQnK-Si_DNonQU-SZqP68OYovZY','answer_pdf_id':'1Cm3pnsKoxiMo6qF-6Ez7MyhVGgVRMvmc'},
  {'exam_id':'2024-9','exam_name':'2024년 9월 모의고사','subject':'수학','exam_date':'2024-09-04','total_questions':30,'question_pdf_id':'1ZuDuBxo3aqTzXfD_XuinHgaLq-8CRRYA','answer_pdf_id':'1eQMivB1GuK5tkWd0oZp07Utu7v_bRZpH'},
  {'exam_id':'2024-6','exam_name':'2024년 6월 모의고사','subject':'수학','exam_date':'2024-06-04','total_questions':30},
  {'exam_id':'2026-3','exam_name':'2026년 3월 모의고사','subject':'수학','exam_date':'2026-03-24','total_questions':30,'question_pdf_id':'1E_lcoi78B_CvTogxxwSShC8CGJ0oUqNp','answer_pdf_id':'12iPNjqLpuhQILuh1jqCPexEcmh0Kd7zn'},
]

result = {'exams': exams, 'questions': questions}
with open(r'C:\Users\user\wrong\tools\ad_math_init.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f'완료! 시험 {len(exams)}개, 문항 {len(questions)}개')
by_id = {}
for q in questions:
    by_id[q['exam_id']] = by_id.get(q['exam_id'], 0) + 1
for k, v in sorted(by_id.items()):
    print(f'  {k}: {v}문항')
