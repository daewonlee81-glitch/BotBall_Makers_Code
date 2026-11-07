import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = os.environ.get('CHROME_PATH') or None
from playwright.sync_api import sync_playwright
import pathlib, json
exec(open(pathlib.Path(__file__).parent/'run.py').read().split('out = {}')[0])
xml = '''<xml xmlns="https://developers.google.com/blockly/xml"><variables><variable id="v1">카운트</variable></variables>
<block type="procedures_defnoreturn" x="0" y="0"><field name="NAME">앞으로</field><statement name="STACK"><block type="variables_set"><field name="VAR" id="v1">카운트</field><value name="VALUE"><block type="math_number"><field name="NUM">5</field></block></value></block></statement></block>
<block type="wombat_start" x="0" y="200"><statement name="DO"><block type="variables_set"><field name="VAR" id="v1">카운트</field><value name="VALUE"><block type="math_arithmetic"><field name="OP">DIVIDE</field><value name="A"><block type="wombat_analog"><field name="PORT">1</field></block></value><value name="B"><block type="math_number"><field name="NUM">2</field></block></value></block></value><next><block type="procedures_callnoreturn"><mutation name="앞으로"></mutation><next><block type="wombat_motor"><field name="PORT">0</field><value name="SPEED"><block type="variables_get"><field name="VAR" id="v1">카운트</field></block></value><next><block type="wombat_servo_slow"><field name="PORT">1</field><value name="POS"><block type="math_number"><field name="NUM">900</field></block></value><value name="STEP"><block type="math_number"><field name="NUM">5</field></block></value></block></next></block></next></block></next></block></statement></block>
<block type="wombat_ao" x="400" y="0"></block></xml>'''
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
    pg = b.new_page(); pg.route('**/*', route); pg.goto((ROOT/'index.html').as_uri()); pg.wait_for_timeout(1200)
    pg.evaluate('x=>WombatBlocks.loadXml(x)', xml); pg.wait_for_timeout(200)
    code = pg.evaluate('WombatBlocks.generateCode()'); print(code)
    json.dump({'var':code}, open(pathlib.Path(__file__).parent/'codes_var.json','w'), ensure_ascii=False)
    b.close()
