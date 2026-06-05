"""
어드민 동기화 서버 — http://localhost:7777
어드민의 "GitHub에 배포" 버튼을 누르면 data/*.json을 저장하고 git push한다.
실행: python tools/sync_server.py
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, subprocess, os, sys, io, base64

# Windows cp949 콘솔에서도 한글/이모지 출력 가능하도록 stdout UTF-8 강제
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, 'data')
PDFS_DIR = os.path.join(ROOT, 'pdfs')
os.makedirs(PDFS_DIR, exist_ok=True)

ID_MAP = {
    'Sat Jun 01 2024 00:00:00 GMT+0900 (Korean Standard Time)': '2024-6',
    'Sun Sep 01 2024 00:00:00 GMT+0900 (Korean Standard Time)': '2024-9',
    'Sun Jun 01 2025 00:00:00 GMT+0900 (Korean Standard Time)': '2025-6',
    'Mon Sep 01 2025 00:00:00 GMT+0900 (Korean Standard Time)': '2025-9',
    'Sun Mar 01 2026 00:00:00 GMT+0900 (Korean Standard Time)': '2026-3',
    '2026-05': '2026-5', '2026_05': '2026-5',
    '2024-06': '2024-6', '2024-09': '2024-9',
    '2025-06': '2025-6', '2025-09': '2025-9',
}

import re
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
SUNEUNG_DATES = {
    '2023-sn': '2022-11-17', '2024-sn': '2023-11-16',
    '2025-sn': '2024-11-14', '2026-sn': '2025-11-13',
}

def norm(data):
    for e in data.get('exams', []):
        e['exam_id'] = ID_MAP.get(e['exam_id'], e['exam_id'])
        # 알려진 수능 날짜 보정
        if e['exam_id'] in SUNEUNG_DATES:
            e['exam_date'] = SUNEUNG_DATES[e['exam_id']]
    for q in data.get('questions', []):
        q['exam_id'] = ID_MAP.get(q['exam_id'], q['exam_id'])
    # 시험일자 내림차순 정렬 (최신 위, 무효 날짜는 뒤)
    def sort_key(e):
        d = e.get('exam_date', '')
        return d if DATE_RE.match(str(d)) else ''
    data['exams'] = sorted(data.get('exams', []), key=sort_key, reverse=True)
    return data

class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200); self._cors(); self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body   = json.loads(self.rfile.read(length))

            # PDF 업로드 분기
            if body.get('type') == 'pdf':
                return self._handle_pdf(body)

            sub    = body.get('subject', '')
            data   = body.get('data', {})

            if sub not in ('korean', 'math', 'english'):
                raise ValueError('unknown subject')

            data = norm(data)
            path = os.path.join(DATA_DIR, sub + '.json')
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f'[저장] {path}  ({len(data["exams"])}시험 {len(data["questions"])}문항)')

            # data + pdfs 모두 git에 추가
            subprocess.run(['git', 'add', path],                      cwd=ROOT, check=True)
            subprocess.run(['git', 'add', 'pdfs/'],                   cwd=ROOT)  # PDF 변경 있으면 같이
            subprocess.run(['git', 'commit', '-m', f'{sub} 데이터 업데이트 (어드민 동기화)'], cwd=ROOT)
            subprocess.run(['git', 'push', 'origin', 'main'],         cwd=ROOT, check=True)
            print('[git push 완료]')

            self.send_response(200); self._cors()
            self.send_header('Content-Type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps({'ok': True, 'exams': len(data['exams']), 'questions': len(data['questions'])}).encode())
        except Exception as e:
            print(f'[오류] {e}')
            self.send_response(500); self._cors(); self.end_headers()
            self.wfile.write(json.dumps({'ok': False, 'error': str(e)}).encode())

    def _handle_pdf(self, body):
        """PDF 파일을 pdfs/ 폴더에 저장."""
        try:
            filename = body.get('filename', '')   # 예: "pdfs/2026_05_영어_q.pdf"
            content_b64 = body.get('content', '') # base64 인코딩된 파일 내용

            if not filename or not filename.startswith('pdfs/'):
                raise ValueError('filename must start with "pdfs/"')
            if '..' in filename or filename.count('/') > 1:
                raise ValueError('invalid filename')

            # base64 헤더(data:application/pdf;base64,) 제거
            if ',' in content_b64:
                content_b64 = content_b64.split(',', 1)[1]
            raw = base64.b64decode(content_b64)

            target_path = os.path.join(ROOT, filename)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, 'wb') as f:
                f.write(raw)

            size_kb = len(raw) // 1024
            print(f'[PDF 저장] {filename}  ({size_kb} KB)')

            self.send_response(200); self._cors()
            self.send_header('Content-Type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps({'ok': True, 'filename': filename, 'size': len(raw)}).encode())
        except Exception as e:
            print(f'[PDF 오류] {e}')
            self.send_response(500); self._cors(); self.end_headers()
            self.wfile.write(json.dumps({'ok': False, 'error': str(e)}).encode())

    def log_message(self, fmt, *args): pass  # 불필요한 로그 억제

PORT = 7777
print(f'=== 어드민 동기화 서버 시작 (포트 {PORT}) ===')
print('어드민에서 "🚀 GitHub에 배포" 버튼을 누르면 자동으로 push됩니다.')
print('종료: Ctrl+C\n')
HTTPServer(('localhost', PORT), Handler).serve_forever()
