import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = os.environ.get('CHROME_PATH') or None
import pathlib
from playwright.sync_api import sync_playwright
NM = ROOT/'node_modules'/'blockly'
def route(r):
    u = r.request.url
    if 'cdn.jsdelivr.net/npm/blockly@13.4.0/' in u:
        p = NM / u.split('blockly@13.4.0/')[1]
        if p.exists(): return r.fulfill(path=str(p), content_type='application/javascript' if p.suffix=='.js' else 'image/svg+xml')
    if u.startswith('file://') or '127.0.0.1' in u: return r.continue_()
    return r.abort()
def out(pg): return pg.inner_text('#consoleOut')
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
    pg = b.new_page(viewport={'width':1440,'height':860})
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route('**/*', route)
    pg.goto((ROOT/'index.html').as_uri()); pg.wait_for_timeout(1200)
    print('run disabled before connect:', pg.is_disabled('#btnRun'))
    # 1) unreachable port
    pg.click('#btnConn'); pg.fill('#ipIn','127.0.0.1'); pg.fill('#portIn','8898'); pg.click('#btnTest'); pg.wait_for_timeout(800)
    print('UNREACHABLE ->', pg.inner_text('#connMsg')[:60])
    # 2) correct
    pg.fill('#portIn','8899'); pg.click('#btnTest'); pg.wait_for_selector('#projSel:not([disabled])', timeout=5000)
    print('CONNECT ->', pg.inner_text('#connMsg'), '| projects:', pg.eval_on_selector_all('#projSel option','els=>els.map(e=>e.value)'))
    pg.select_option('#userSel','teacher'); pg.wait_for_timeout(500)
    print('TEACHER ->', pg.inner_text('#connMsg')[:70], '| ok disabled:', pg.is_disabled('#btnConnOk'))
    pg.select_option('#userSel','학생1'); pg.wait_for_selector('#projSel:not([disabled])')
    pg.screenshot(path=str(pathlib.Path(__file__).parent)+'/e2e_modal.png')
    pg.click('#btnConnOk'); pg.wait_for_timeout(300)
    print('header label:', pg.inner_text('#connLbl'), '| run enabled:', not pg.is_disabled('#btnRun'))
    # 3) run example 1 to completion
    pg.evaluate('WombatBlocks.loadXml(WombatBlocks.EXAMPLES[0].xml)'); pg.wait_for_timeout(300)
    pg.click('#btnRun')
    pg.wait_for_function("document.querySelector('#consoleOut').innerText.includes('프로그램이 끝났습니다')", timeout=15000)
    print('RUN1 console:\n', out(pg))
    pg.screenshot(path=str(pathlib.Path(__file__).parent)+'/e2e_run.png')
    saved = (ROOT/'mock'/'kiss'/'학생1'/'블록코딩'/'src'/'main.py').read_text()
    print('saved main.py matches code:', saved == pg.evaluate('WombatBlocks.generateCode()'))
    # 4) infinite loop + stop
    pg.click('#btnClearConsole')
    pg.evaluate('WombatBlocks.loadXml(WombatBlocks.EXAMPLES[2].xml)'); pg.wait_for_timeout(300)
    pg.keyboard.press('Control+Enter'); pg.wait_for_timeout(1500)
    print('running? stop enabled:', not pg.is_disabled('#btnStop'), '| live badge:', pg.eval_on_selector('#tabConsole','e=>e.classList.contains("live")'))
    pg.click('#btnStop'); pg.wait_for_timeout(600)
    print('STOP tail:', out(pg).strip().split('\n')[-2:], '| stop disabled after:', pg.is_disabled('#btnStop'))
    # 5) compile error path (corrupt saved code)
    pg.click('#btnClearConsole')
    pg.evaluate('''()=>{const f=window.fetch; window.fetch=(u,o)=>{ if(String(u).includes('save-file-content')){const b=JSON.parse(o.body); b.fileContents+='\\ndef broken(:\\n'; o={...o, body:JSON.stringify(b)};} return f(u,o);};}''')
    pg.click('#btnRun'); pg.wait_for_timeout(1500)
    print('COMPILE ERR console:\n', out(pg))
    print('page errors:', errs)
    b.close()
print(open(ROOT/'mock'/'requests.log').read().replace('\n',' | '))
