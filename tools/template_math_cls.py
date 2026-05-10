import json

# 수학 공통(1-22) + 선택(23-30) = 30문항 = 100점
# 공통 배점: 객관식 2점(1-9) 3점(10-15) + 단답형 3점(16) 4점(17-22)
# 선택 배점: 객관식 2점(23-25) 3점(26-28) + 단답형 4점(29-30)

# 공통 배점: 2점(1-4 = 4개), 3점(5-10 = 6개), 4점(11-22 = 12개) → 8+18+48 = 74점
common_topics = {
    1:  ('수학I', '지수와 로그', 2),
    2:  ('수학I', '삼각함수', 2),
    3:  ('수학I', '수열', 2),
    4:  ('수학II', '함수의 극한', 2),
    5:  ('수학I', '지수와 로그', 3),
    6:  ('수학I', '삼각함수', 3),
    7:  ('수학I', '수열', 3),
    8:  ('수학II', '함수의 극한', 3),
    9:  ('수학II', '미분', 3),
    10: ('수학II', '적분', 3),
    11: ('수학I', '지수와 로그', 4),
    12: ('수학I', '삼각함수', 4),
    13: ('수학I', '수열', 4),
    14: ('수학II', '함수의 극한', 4),
    15: ('수학II', '미분', 4),
    16: ('수학II', '적분', 4),
    17: ('수학I', '수열', 4),      # 단답형 시작
    18: ('수학II', '미분', 4),
    19: ('수학II', '적분', 4),
    20: ('수학I', '삼각함수', 4),
    21: ('수학II', '미분', 4),
    22: ('수학II', '적분', 4),
}

# 선택 배점: 2점(23-24 = 2개), 3점(25-26 = 2개), 4점(27-30 = 4개) → 4+6+16 = 26점

# 선택: 확통
hwaktong = {
    23: ('확률과통계', '경우의 수', 2),
    24: ('확률과통계', '확률', 2),
    25: ('확률과통계', '통계', 3),
    26: ('확률과통계', '경우의 수', 3),
    27: ('확률과통계', '확률', 4),
    28: ('확률과통계', '통계', 4),
    29: ('확률과통계', '확률', 4),
    30: ('확률과통계', '통계', 4),
}

# 선택: 미적분
mijeok = {
    23: ('미적분', '수열의 극한', 2),
    24: ('미적분', '미분법', 2),
    25: ('미적분', '적분법', 3),
    26: ('미적분', '수열의 극한', 3),
    27: ('미적분', '미분법', 4),
    28: ('미적분', '적분법', 4),
    29: ('미적분', '미분법', 4),
    30: ('미적분', '적분법', 4),
}

# 선택: 기하
giha = {
    23: ('기하', '이차곡선', 2),
    24: ('기하', '벡터', 2),
    25: ('기하', '공간도형', 3),
    26: ('기하', '이차곡선', 3),
    27: ('기하', '벡터', 4),
    28: ('기하', '공간도형', 4),
    29: ('기하', '벡터', 4),
    30: ('기하', '공간도형', 4),
}

def make_cls(choice_name, choice_sec, choice_data):
    cls = []
    for q in range(1, 23):
        topic, subtopic, score = common_topics[q]
        cls.append({'q': q, 'section': 'common', 'topic': topic, 'subtopic': subtopic, 'score': score})
    for q in range(23, 31):
        topic, subtopic, score = choice_data[q]
        cls.append({'q': q, 'section': choice_sec, 'topic': topic, 'subtopic': subtopic, 'score': score})
    total = sum(x['score'] for x in cls)
    print(f'수학({choice_name}) {len(cls)}문항: {total}점')
    return cls

for name, sec, data, fname in [
    ('확률과통계', 'hwaktong', hwaktong, 'template_math_hwaktong_cls.json'),
    ('미적분',     'mijeok',   mijeok,   'template_math_mijeok_cls.json'),
    ('기하',       'giha',     giha,     'template_math_giha_cls.json'),
]:
    cls = make_cls(name, sec, data)
    with open(f'tools/{fname}', 'w', encoding='utf-8') as f:
        json.dump(cls, f, ensure_ascii=False, indent=2)
