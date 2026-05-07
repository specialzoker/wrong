# 수능 오답 유사문제 추천

국어·수학·영어 오답 유사문제 추천 웹사이트입니다.

---

## 폴더 구조

```
/
├── index.html          ← 메인 허브 (과목 선택 화면)
├── korean/index.html   ← 국어 앱
├── math/index.html     ← 수학 앱
├── english/index.html  ← 영어 앱
└── data/
    ├── korean.json     ← 국어 시험·문항 데이터 (직접 편집)
    ├── math.json       ← 수학 시험·문항 데이터 (직접 편집)
    └── english.json    ← 영어 시험·문항 데이터 (직접 편집)
```

---

## JSON 데이터 편집 방법

### 1. 시험 추가 (`exams` 배열)

```json
{
  "exam_id": "2025_수능",
  "exam_name": "2025학년도 수능",
  "subject": "국어",
  "exam_date": "2024-11-14",
  "total_questions": 45,
  "question_pdf_id": "구글드라이브_파일ID",
  "answer_pdf_id": "구글드라이브_정답파일ID"
}
```

**구글 드라이브 파일 ID 찾는 법:**
구글 드라이브 공유 링크에서 `/d/` 뒤의 문자열이 파일 ID입니다.
```
https://drive.google.com/file/d/【여기가_파일_ID】/view
```

### 2. 문항 추가 (`questions` 배열)

**국어/수학 `is_common` 값:**
| 값 | 의미 |
|---|---|
| `"공통"` | 공통과목 |
| `"화법과작문"` | 국어 화법과작문 선택 |
| `"언어와매체"` | 국어 언어와매체 선택 |
| `"선택-확통"` | 수학 확률과통계 선택 |
| `"선택-미적분"` | 수학 미적분 선택 |
| `"선택-기하"` | 수학 기하 선택 |

**영어 `section` 값:** `"듣기"` 또는 `"독해"`

**`difficulty` 값:** `"하"`, `"중"`, `"상"`

---

## GitHub Pages 배포 방법

### 처음 설정 (1회만)

1. GitHub에서 새 저장소(repository) 생성
2. 이 폴더의 파일을 모두 push
   ```bash
   git init
   git add .
   git commit -m "첫 번째 배포"
   git remote add origin https://github.com/사용자명/저장소명.git
   git push -u origin main
   ```
3. GitHub 저장소 → **Settings** → **Pages**
4. **Source**: `GitHub Actions` 선택 → 저장

배포 완료 후 주소: `https://사용자명.github.io/저장소명/`

### 데이터 업데이트

JSON 파일을 수정한 뒤:
```bash
git add data/korean.json
git commit -m "국어 2025 수능 데이터 추가"
git push
```
→ 약 1~2분 후 자동으로 사이트에 반영됩니다.

---

## 로컬에서 미리보기

파일을 직접 브라우저로 열면 fetch가 차단됩니다. 로컬 웹서버를 사용하세요.

**방법 1 — Python (추천):**
```bash
python -m http.server 8000
# 브라우저에서 http://localhost:8000 접속
```

**방법 2 — VS Code:**
Live Server 확장 설치 후 `index.html`에서 우클릭 → `Open with Live Server`

---

## 오답 기록

학생 이름 + 오답 번호가 각 과목별로 브라우저 `localStorage`에 자동 저장됩니다.
(이전 Google Sheets `오답기록` 시트 대체)

---

Made by 정현석 (광명북고 진로진학부장 · 경기진협 자료개발국 간사)
