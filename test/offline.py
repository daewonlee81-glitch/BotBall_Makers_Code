import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = os.environ.get('CHROME_PATH') or None
from playwright.sync_api import sync_playwright
blocked=[]
def route(r):
    u=r.request.url
    if u.startswith('file://') or u.startswith('data:') or '127.0.0.1' in u: return r.continue_()
    blocked.append(u.split('?')[0][:80]); return r.abort()
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1440,'height':860}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/*',route)
    pg.goto((ROOT/'index.html').as_uri()); pg.wait_for_timeout(1500)
    print('Blockly loaded offline:', pg.evaluate('!!window.Blockly && !!window.WombatBlocks'), '| error panel shown:', pg.is_visible('#loadErr'))
    print('toolbox label:', pg.locator('.blocklyToolboxCategoryLabel').first.inner_text())
    print('images using embedded data:', pg.evaluate("[...document.querySelectorAll('#blocklyDiv image')].map(i=>(i.getAttribute('href')||'').slice(0,22))"))
    print('code lines:', pg.evaluate('WombatBlocks.generateCode().split("\\n").length'))
    pg.screenshot(path=str(pathlib.Path(__file__).parent)+'/offline.png')
    print('page errors:', errs)
    print('blocked external requests:', sorted(set(blocked)))
    b.close()
