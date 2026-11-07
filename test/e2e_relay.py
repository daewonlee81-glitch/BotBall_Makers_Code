import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = os.environ.get('CHROME_PATH') or None
import pathlib, time
from playwright.sync_api import sync_playwright
HW = (ROOT/'mock-harrogate'/'ws')
def route(r):
    u = r.request.url
    if u.startswith('file://') or '127.0.0.1' in u or 'localhost' in u: return r.continue_()
    return r.abort()
out = lambda pg: pg.inner_text('#consoleOut')
def connect(pg, ip, port, user=None):
    (pg.click('#btnConn') if pg.is_hidden('#connModal') else None); pg.fill('#ipIn', ip); pg.fill('#portIn', str(port)); pg.click('#btnTest')
    pg.wait_for_function("(()=>{const m=document.querySelector('#connMsg'); return m.classList.contains('err') || m.innerText.includes('프로젝트')})()", timeout=10000)
    if user:
        pg.wait_for_selector('#userSel:not([disabled])', timeout=5000); pg.select_option('#userSel', user); pg.wait_for_function("document.querySelector('#connMsg').innerText.includes('"+user+"')", timeout=5000)
    return pg.inner_text('#connMsg')
def wait_out(pg, text, t=15000):
    try: pg.wait_for_function(f"document.querySelector('#consoleOut').innerText.includes({text!r})", timeout=t)
    except Exception:
        print('---- CONSOLE DUMP ----'); print(pg.inner_text('#consoleOut')[-1500:]); print('---- requests ----'); print(open(ROOT/'mock-harrogate'/'requests.log').read()[-800:]); raise
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
    errs = []
    # A) 파일로 연 웹앱 → Harrogate 직접: CORS 차단 안내
    pg = b.new_page(); pg.on('pageerror', lambda e: errs.append(str(e))); pg.route('**/*', route)
    pg.goto((ROOT/'index.html').as_uri()); pg.wait_for_timeout(1000)
    print('A direct→harrogate:', connect(pg, '127.0.0.1', 8898)[:70])
    # A2) 파일 → Voldigate 직접 (회귀)
    print('A2 direct→voldigate:', connect(pg, '127.0.0.1', 8899)[:60])
    pg.close()
    # B) 연결 도우미로 연 웹앱 → Harrogate
    pg = b.new_page(viewport={'width':1440,'height':860}); pg.on('pageerror', lambda e: errs.append(str(e))); pg.route('**/*', route)
    pg.goto('http://127.0.0.1:8765/'); pg.wait_for_timeout(1500)
    pg.click('#btnConn'); pg.wait_for_timeout(200)
    print('B viaNote:', pg.inner_text('#viaNote')[:40], '| ip prefilled:', pg.input_value('#ipIn'), pg.input_value('#portIn'))
    pg.click('#btnConnClose')
    msg = connect(pg, '127.0.0.1', 8898, '학생1')
    print('B connect:', msg[:80], '| projects:', pg.eval_on_selector_all('#projSel option', 'e=>e.map(x=>x.value)'))
    pg.screenshot(path=str(pathlib.Path(__file__).parent/'relay_modal.png'))
    pg.click('#btnConnOk'); pg.wait_for_timeout(800)
    pg.evaluate('WombatBlocks.loadXml(WombatBlocks.EXAMPLES[0].xml)'); pg.wait_for_timeout(300)
    pg.click('#btnRun'); wait_out(pg, '프로그램이 끝났습니다')
    print('B run console:\n', '\n'.join(l for l in out(pg).split('\n') if not l.startswith('[kipr]')))
    saved = (HW/'학생1'/'블록코딩'/'src'/'main.py').read_text(encoding='utf-8')
    print('B saved main.py == generated:', saved == pg.evaluate('WombatBlocks.generateCode()'), '| has Korean:', '안녕' in saved)
    pg.screenshot(path=str(pathlib.Path(__file__).parent/'relay_run.png'))
    # 정지 (무한 반복 예제)
    pg.click('#btnClearConsole'); pg.evaluate('WombatBlocks.loadXml(WombatBlocks.EXAMPLES[2].xml)'); pg.wait_for_timeout(300)
    pg.click('#btnRun'); wait_out(pg, '실행 시작'); pg.wait_for_timeout(1500)
    print('B running, stop enabled:', not pg.is_disabled('#btnStop'))
    pg.click('#btnStop'); pg.wait_for_timeout(1500)
    tail = out(pg).strip().split('\n')[-3:]
    print('B stop tail:', tail, '| ao() called after stop:', any('ao()' in l for l in out(pg).split('\n')[-5:]), '| stop disabled:', pg.is_disabled('#btnStop'))
    # 다시 실행(중복 실행 409 처리 포함) 후 정상 종료
    pg.click('#btnClearConsole'); pg.evaluate('WombatBlocks.loadXml(WombatBlocks.EXAMPLES[1].xml)'); pg.wait_for_timeout(300)
    pg.evaluate("document.querySelector('#btnRun').click()"); wait_out(pg, '프로그램이 끝났습니다', 20000)
    print('B second run ok')
    # 문법 오류
    pg.click('#btnClearConsole')
    pg.evaluate('''()=>{const f=window.fetch; window.fetch=(u,o)=>{ if(o&&o.method==='PUT'){const bd=JSON.parse(o.body); const s=new TextDecoder().decode(Uint8Array.from(atob(bd.content),c=>c.charCodeAt(0)))+'\\ndef broken(:\\n'; bd.content=btoa(String.fromCharCode(...new TextEncoder().encode(s))); o={...o,body:JSON.stringify(bd)};} return f(u,o);};}''')
    pg.click('#btnRun'); pg.wait_for_timeout(2000)
    print('B compile error:', [l for l in out(pg).split('\n') if '오류' in l or 'SyntaxError' in l][:3])
    pg.reload(); pg.wait_for_timeout(1500)
    # main.py 없는 프로젝트(POST로 새로 만들기)
    connect(pg, '127.0.0.1', 8898, 'Default User'); pg.click('#btnConnOk'); pg.wait_for_timeout(600)
    pg.click('#btnSendOnly'); wait_out(pg, '문법 검사 통과')
    print('B new main.py created:', (HW/'Default User'/'빈프로젝트'/'src'/'main.py').exists())
    # C) 연결 도우미 → Voldigate
    msg = connect(pg, '127.0.0.1', 8899)
    print('C relay→voldigate:', msg[:70]); pg.click('#btnConnOk'); pg.wait_for_timeout(500)
    pg.click('#btnClearConsole'); pg.evaluate('WombatBlocks.loadXml(WombatBlocks.EXAMPLES[0].xml)'); pg.wait_for_timeout(300)
    pg.click('#btnRun'); wait_out(pg, '프로그램이 끝났습니다')
    print('C run ok:', out(pg).count('[kipr]') > 3, '| target:', pg.inner_text('#consoleTarget'))
    print('page errors:', errs)
    b.close()
