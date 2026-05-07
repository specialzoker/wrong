// ====================================================
// 수학 데이터 JSON 내보내기 스크립트
// 사용법: 수학 앱스크립트 프로젝트에 이 코드를 붙여넣고
//         상단 메뉴 [실행] → exportToJson 실행
// ====================================================

function exportToJson() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  // ── 모의고사 목록 읽기 ──
  var examSheet = ss.getSheetByName('모의고사목록');
  if (!examSheet) { SpreadsheetApp.getUi().alert('시트를 찾을 수 없습니다: 모의고사목록'); return; }
  var examData = examSheet.getDataRange().getValues();
  var exams = [];

  for (var i = 1; i < examData.length; i++) {
    var row = examData[i];
    if (!row[0]) continue;
    exams.push({
      exam_id:         String(row[0]),
      exam_name:       String(row[1]),
      subject:         String(row[2]),
      exam_date:       String(row[3]),
      total_questions: row[4] || 30,
      question_pdf_id: extractDriveId(row[6]),  // 수학: G열 (index 6)
      answer_pdf_id:   extractDriveId(row[8])   // 수학: I열 (index 8)
    });
  }

  // ── 문항 정보 읽기 ──
  var qSheet = ss.getSheetByName('문항정보');
  if (!qSheet) { SpreadsheetApp.getUi().alert('시트를 찾을 수 없습니다: 문항정보'); return; }
  var qData = qSheet.getDataRange().getValues();
  var questions = [];

  for (var i = 1; i < qData.length; i++) {
    if (!qData[i][0]) continue;
    questions.push({
      exam_id:        String(qData[i][0]),
      question_no:    qData[i][1],
      topic:          String(qData[i][2]),
      subtopic:       String(qData[i][3]),
      difficulty:     String(qData[i][4]),
      keywords:       String(qData[i][5]),
      question_page:  qData[i][6],
      answer_page:    qData[i][7],
      correct_answer: String(qData[i][8]),
      score:          qData[i][9],
      is_common:      String(qData[i][10])  // '공통' / '선택-확통' / '선택-미적분' / '선택-기하'
    });
  }

  var output = JSON.stringify({ exams: exams, questions: questions }, null, 2);
  showJsonDialog(output, 'math.json');
}

function extractDriveId(input) {
  if (!input) return '';
  input = String(input).trim();
  if (!input) return '';
  var m1 = input.match(/\/d\/([a-zA-Z0-9_-]{25,})/);
  if (m1) return m1[1];
  var m2 = input.match(/[?&]id=([a-zA-Z0-9_-]{25,})/);
  if (m2) return m2[1];
  if (input.indexOf('/') < 0 && input.length >= 25) return input;
  return '';
}

function showJsonDialog(jsonText, filename) {
  var safe = jsonText.replace(/</g, '\\u003c').replace(/>/g, '\\u003e');
  var html = '<html><head><style>'
    + 'body{font-family:monospace;font-size:11px;padding:10px;margin:0}'
    + 'textarea{width:100%;height:calc(100vh - 60px);border:1px solid #ccc;font-size:11px;padding:8px;resize:none}'
    + 'button{padding:8px 18px;background:#2d5a27;color:white;border:none;border-radius:4px;cursor:pointer;font-size:13px;margin-bottom:8px}'
    + 'p{font-size:12px;color:#555;margin:0 0 6px}'
    + '</style></head><body>'
    + '<p>아래 내용을 전체 복사(Ctrl+A → Ctrl+C) 후 <strong>data/' + filename + '</strong> 파일에 붙여넣으세요.</p>'
    + '<button onclick="sel()">전체 선택</button>'
    + '<textarea id="o">' + safe + '</textarea>'
    + '<script>function sel(){var t=document.getElementById("o");t.select();}<\/script>'
    + '</body></html>';
  SpreadsheetApp.getUi().showModalDialog(
    HtmlService.createHtmlOutput(html).setWidth(920).setHeight(620),
    filename + ' 내보내기'
  );
}
