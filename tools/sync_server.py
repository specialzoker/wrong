"""
어드민 동기화 서버 — http://localhost:7777
어드민의 "GitHub에 배포" 버튼을 누르면 data/*.json을 저장하고 git push한다.
실행: python tools/sync_server.py
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, subprocess, os, sys, io

# Windows cp949 콘솔에서도 한글/이모지 출력 가능하도록 stdout UTF-8 강제
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, 'data')

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

def norm(data):
    for e in data.get('exams', []):
        e['exam_id'] = ID_MAP.get(e['exam_id'], e['exam_id'])
    for q in data.get('questions', []):
        q['exam_id'] = ID_MAP.get(q['exam_id'], q['exam_id'])
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
            sub    = body.get('subject', '')
            data   = body.get('data', {})

            if sub not in ('korean', 'math', 'english'):
                raise ValueError('unknown subject')

            data = norm(data)
            path = os.path.join(DATA_DIR, sub + '.json')
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f'[저장] {path}  ({len(data["exams"])}시험 {len(data["questions"])}문항)')

            subprocess.run(['git', 'add', path],                      cwd=ROOT, check=True)
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

    def log_message(self, fmt, *args): pass  # 불필요한 로그 억제

PORT = 7777
print(f'=== 어드민 동기화 서버 시작 (포트 {PORT}) ===')
print('어드민에서 "🚀 GitHub에 배포" 버튼을 누르면 자동으로 push됩니다.')
print('종료: Ctrl+C\n')
HTTPServer(('localhost', PORT), Handler).serve_forever()
