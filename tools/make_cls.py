import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

cls = [
  # 공통 (1-34)
  {"q":1,"section":"common","topic":"독서","subtopic":"내용 파악","score":2,"keywords":"이항 대립 구조, 개념 분석"},
  {"q":2,"section":"common","topic":"독서","subtopic":"내용 파악","score":3,"keywords":"이항 대립 구조, 홍길동전"},
  {"q":3,"section":"common","topic":"독서","subtopic":"어휘","score":2,"keywords":"이항 대립 구조, 어휘 의미"},
  {"q":4,"section":"common","topic":"독서","subtopic":"내용 파악","score":2,"keywords":"러셀, 명제론, 언어 게임"},
  {"q":5,"section":"common","topic":"독서","subtopic":"내용 파악","score":2,"keywords":"러셀, 리오타르, 언어 게임"},
  {"q":6,"section":"common","topic":"독서","subtopic":"내용 파악","score":2,"keywords":"러셀, 직접적 인식, 언어 게임"},
  {"q":7,"section":"common","topic":"독서","subtopic":"내용 파악","score":2,"keywords":"리오타르, 언어 게임, 공약불가능성"},
  {"q":8,"section":"common","topic":"독서","subtopic":"내용 파악","score":3,"keywords":"러셀, 리오타르, 구체적 사례 적용"},
  {"q":9,"section":"common","topic":"독서","subtopic":"어휘","score":2,"keywords":"리오타르, 어휘 의미"},
  {"q":10,"section":"common","topic":"독서","subtopic":"내용 파악","score":2,"keywords":"볼록 렌즈, 비점수차, 상점"},
  {"q":11,"section":"common","topic":"독서","subtopic":"내용 파악","score":2,"keywords":"비점수차, 자오면, 구결면"},
  {"q":12,"section":"common","topic":"독서","subtopic":"내용 파악","score":2,"keywords":"볼록 렌즈, 비점수차, 이유 파악"},
  {"q":13,"section":"common","topic":"독서","subtopic":"내용 파악","score":3,"keywords":"볼록 렌즈, 비점수차, 최소 착란원"},
  {"q":14,"section":"common","topic":"독서","subtopic":"내용 파악","score":2,"keywords":"구분소유권, 집합건물, 전유부분"},
  {"q":15,"section":"common","topic":"독서","subtopic":"내용 파악","score":2,"keywords":"구분소유권, 공용부분, 지분"},
  {"q":16,"section":"common","topic":"독서","subtopic":"내용 파악","score":3,"keywords":"구분소유권, 구체적 적용"},
  {"q":17,"section":"common","topic":"독서","subtopic":"어휘","score":2,"keywords":"구분소유권, 어휘 의미"},
  {"q":18,"section":"common","topic":"현대소설","subtopic":"표현 기법","score":2,"keywords":"사환아이, 서술 방식"},
  {"q":19,"section":"common","topic":"현대소설","subtopic":"표현 기법","score":2,"keywords":"사환아이, 서술 방식 ㉠~㉤"},
  {"q":20,"section":"common","topic":"현대소설","subtopic":"내용 파악","score":2,"keywords":"사환아이, ⓐⓑ 분석"},
  {"q":21,"section":"common","topic":"현대소설","subtopic":"외적 준거","score":3,"keywords":"사환아이, 종합 감상"},
  {"q":22,"section":"common","topic":"복합지문","subtopic":"표현 기법","score":2,"keywords":"현대시(안개), 고전산문(난초)"},
  {"q":23,"section":"common","topic":"현대시","subtopic":"표현 기법","score":2,"keywords":"안개, ㉠~㉤ 표현 분석"},
  {"q":24,"section":"common","topic":"복합지문","subtopic":"외적 준거","score":3,"keywords":"안개, 시적 상상력, 보기 감상"},
  {"q":25,"section":"common","topic":"고전산문","subtopic":"내용 파악","score":2,"keywords":"난초, 주인, 객, 내용 이해"},
  {"q":26,"section":"common","topic":"복합지문","subtopic":"표현 기법","score":2,"keywords":"안개, 난초, 감상 비교"},
  {"q":27,"section":"common","topic":"복합지문","subtopic":"표현 기법","score":2,"keywords":"고전시가(영회잡곡), (가)~(다) 표현"},
  {"q":28,"section":"common","topic":"고전시가","subtopic":"시어의 의미","score":2,"keywords":"영회잡곡, 시어 분석, 백발"},
  {"q":29,"section":"common","topic":"고전시가","subtopic":"내용 파악","score":2,"keywords":"영회잡곡, 노년, 내용 이해"},
  {"q":30,"section":"common","topic":"복합지문","subtopic":"외적 준거","score":3,"keywords":"고전시가, 노년의 삶, 보기 감상"},
  {"q":31,"section":"common","topic":"고전소설","subtopic":"내용 파악","score":2,"keywords":"방주, 효열부인, 내용 이해"},
  {"q":32,"section":"common","topic":"고전소설","subtopic":"표현 기법","score":2,"keywords":"방주, 효열부인, 서술 방식"},
  {"q":33,"section":"common","topic":"고전소설","subtopic":"인물 분석","score":2,"keywords":"방주, 효열부인, ㉠~㉢ 인물"},
  {"q":34,"section":"common","topic":"고전소설","subtopic":"외적 준거","score":3,"keywords":"방주, 효열부인, 종합 감상"},
  # 화법과작문 (35-45)
  {"q":35,"section":"hwajak","topic":"화법","subtopic":"말하기 방식","score":2,"keywords":"발표, 흉배, 왕실 복식"},
  {"q":36,"section":"hwajak","topic":"화법","subtopic":"자료 활용","score":2,"keywords":"발표, 흉배, 자료 제시"},
  {"q":37,"section":"hwajak","topic":"화법","subtopic":"반응 이해","score":2,"keywords":"발표, 흉배, 청중 반응"},
  {"q":38,"section":"hwajak","topic":"작문","subtopic":"내용 생성","score":2,"keywords":"건의문, 텃밭 잡초, 토끼풀"},
  {"q":39,"section":"hwajak","topic":"작문","subtopic":"고쳐쓰기","score":3,"keywords":"건의문, 고쳐쓰기 계획"},
  {"q":40,"section":"hwajak","topic":"화법","subtopic":"대화 분석","score":2,"keywords":"건의문, 동아리 대화"},
  {"q":41,"section":"hwajak","topic":"화법","subtopic":"대화 분석","score":2,"keywords":"건의문, 학생 대화 분석"},
  {"q":42,"section":"hwajak","topic":"작문","subtopic":"말하기 방식","score":2,"keywords":"건의문, [A][B] 대화 분석"},
  {"q":43,"section":"hwajak","topic":"작문","subtopic":"글쓰기 계획","score":2,"keywords":"사운드스케이프, 쓰기 계획"},
  {"q":44,"section":"hwajak","topic":"작문","subtopic":"내용 생성","score":2,"keywords":"사운드스케이프, 내용 수정"},
  {"q":45,"section":"hwajak","topic":"작문","subtopic":"자료 활용","score":3,"keywords":"사운드스케이프, 자료 활용"},
  # 언어와매체 (35-45)
  {"q":35,"section":"eonmae","topic":"언어","subtopic":"단어 형성","score":2,"keywords":"용언, 있다, 동사, 형용사"},
  {"q":36,"section":"eonmae","topic":"언어","subtopic":"문법 요소","score":3,"keywords":"용언, 있다, 중세 국어 탐구"},
  {"q":37,"section":"eonmae","topic":"언어","subtopic":"음운 변동","score":2,"keywords":"음운 변동, 음절 구조"},
  {"q":38,"section":"eonmae","topic":"언어","subtopic":"음운 변동","score":2,"keywords":"흙일, 짓밟다, 직행열차"},
  {"q":39,"section":"eonmae","topic":"언어","subtopic":"문장 구조","score":2,"keywords":"음운 변동, 탐구 적용"},
  {"q":40,"section":"eonmae","topic":"매체","subtopic":"매체 특성","score":2,"keywords":"가짜 뉴스, TV 방송, 허위 조작 정보"},
  {"q":41,"section":"eonmae","topic":"매체","subtopic":"매체 특성","score":2,"keywords":"가짜 뉴스, 시청자 수용 양상"},
  {"q":42,"section":"eonmae","topic":"매체","subtopic":"매체 언어","score":2,"keywords":"가짜 뉴스, 발표 자료 비교"},
  {"q":43,"section":"eonmae","topic":"매체","subtopic":"매체 특성","score":2,"keywords":"가짜 뉴스, 내용 분석"},
  {"q":44,"section":"eonmae","topic":"매체","subtopic":"매체 특성","score":2,"keywords":"온라인 게시판, 누리 소통망"},
  {"q":45,"section":"eonmae","topic":"매체","subtopic":"매체 특성","score":3,"keywords":"온라인 게시판, 가상 게시판"},
]

common = [x for x in cls if x["section"]=="common"]
hwajak = [x for x in cls if x["section"]=="hwajak"]
eonmae = [x for x in cls if x["section"]=="eonmae"]
sc = sum(x["score"] for x in common)
sh = sum(x["score"] for x in hwajak)
se = sum(x["score"] for x in eonmae)
print(f"공통 {len(common)}문항: {sc}점")
print(f"화작 {len(hwajak)}문항: {sh}점  → 합계: {sc+sh}점")
print(f"언매 {len(eonmae)}문항: {se}점  → 합계: {sc+se}점")
print()
print(json.dumps(cls, ensure_ascii=False, indent=2))
