import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = os.environ.get('CHROME_PATH') or None
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=['--no-sandbox']); pg=b.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/*',lambda r: r.continue_() if '127.0.0.1' in r.request.url else r.abort())
    pg.goto('http://127.0.0.1:8898/wombat-blocks.html'); pg.wait_for_timeout(2000)
    pg.click('#btnConn'); pg.wait_for_timeout(300)
    print('viaNote:', pg.inner_text('#viaNote')[:50], '| ip disabled:', pg.is_disabled('#ipIn'))
    pg.click('#btnTest'); pg.wait_for_selector('#userSel:not([disabled])'); pg.select_option('#userSel','학생1')
    pg.wait_for_function("document.querySelector('#connMsg').innerText.includes('학생1')"); pg.click('#btnConnOk'); pg.wait_for_timeout(600)
    pg.evaluate('WombatBlocks.loadXml(WombatBlocks.EXAMPLES[0].xml)'); pg.wait_for_timeout(300); pg.click('#btnRun')
    pg.wait_for_function("document.querySelector('#consoleOut').innerText.includes('프로그램이 끝났습니다')", timeout=15000)
    print('same-origin run ok | target:', pg.inner_text('#consoleTarget')); print('errors:', errs); b.close()
