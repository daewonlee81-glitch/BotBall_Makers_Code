import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = os.environ.get('CHROME_PATH') or None
import json, sys, pathlib
from playwright.sync_api import sync_playwright
NM = ROOT/'node_modules'/'blockly'
def route(r):
    u = r.request.url
    if 'cdn.jsdelivr.net/npm/blockly@13.4.0/' in u:
        rel = u.split('blockly@13.4.0/')[1]
        p = NM / rel
        if p.exists():
            ct = 'application/javascript' if p.suffix == '.js' else ('image/svg+xml' if p.suffix=='.svg' else 'application/octet-stream')
            return r.fulfill(path=str(p), content_type=ct)
    if u.startswith('file://'): return r.continue_()
    return r.abort()
out = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
    pg = b.new_page(viewport={'width':1440,'height':860})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: m.type=='error' and errs.append(m.text))
    pg.route('**/*', route)
    pg.goto((ROOT/'index.html').as_uri())
    pg.wait_for_timeout(1500)
    n = pg.evaluate('WombatBlocks.EXAMPLES.length')
    for i in range(n):
        pg.evaluate(f'WombatBlocks.loadXml(WombatBlocks.EXAMPLES[{i}].xml)')
        pg.wait_for_timeout(150)
        name = pg.evaluate(f'WombatBlocks.EXAMPLES[{i}].name')
        out[name] = pg.evaluate('WombatBlocks.generateCode()')
    # every toolbox block: place each block type in a start block one at a time
    types = pg.evaluate('''Object.keys(Blockly.Blocks).filter(t=>t.startsWith('wombat_') && t!=='wombat_start')''')
    for t in types:
        code = pg.evaluate('''(t)=>{const ws=WombatBlocks.ws; ws.clear();
          const s=ws.newBlock('wombat_start'); s.initSvg(); s.render();
          const b=ws.newBlock(t); b.initSvg(); b.render();
          // fill number inputs with literal blocks
          b.inputList.forEach(inp=>{ if(inp.connection && inp.type===1){ const n=ws.newBlock('math_number'); n.setFieldValue('2','NUM'); n.initSvg(); n.render(); inp.connection.connect(n.outputConnection);} });
          if (b.previousConnection) s.getInput('DO').connection.connect(b.previousConnection);
          else { const p=ws.newBlock('wombat_print'); p.initSvg(); p.render(); s.getInput('DO').connection.connect(p.previousConnection); p.getInput('TEXT').connection.connect(b.outputConnection); }
          return WombatBlocks.generateCode(); }''', t)
        out['block:'+t] = code
    pg.evaluate('WombatBlocks.loadXml(WombatBlocks.EXAMPLES[2].xml)')
    pg.wait_for_timeout(400)
    pg.screenshot(path=str(pathlib.Path(__file__).parent)+'/shot_main.png')
    pg.locator('.blocklyToolboxCategory').nth(1).click(force=True)
    pg.wait_for_timeout(400)
    pg.screenshot(path=str(pathlib.Path(__file__).parent)+'/shot_motor.png')
    print('page errors:', errs)
    b.close()
json.dump(out, open(pathlib.Path(__file__).parent/'codes.json','w'), ensure_ascii=False, indent=1)
print('programs:', len(out))
