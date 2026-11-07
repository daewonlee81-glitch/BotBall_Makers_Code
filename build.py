# app.src.html → index.html (Blockly·아이콘을 파일 안에 내장: 인터넷 없이 동작)
import base64, pathlib, re
B = pathlib.Path('node_modules/blockly'); VER='13.4.0'
s = pathlib.Path('app.src.html').read_text(encoding='utf-8')
media = {n: 'data:image/svg+xml;base64,' + base64.b64encode((B/'media'/n).read_bytes()).decode() for n in ['sprites.svg','delete-icon.svg','foldout-icon.svg','resize-handle.svg','dropdown-arrow.svg']}
import json
for f in ['blockly_compressed.js','blocks_compressed.js','python_compressed.js','msg/ko.js']:
    tag = f'<script src="https://cdn.jsdelivr.net/npm/blockly@{VER}/{f}"></script>'
    assert s.count(tag)==1, f
    js = (B/f).read_text(encoding='utf-8')
    assert '</script' not in js.lower()
    s = s.replace(tag, f'<script>/* Blockly {VER} {f} — Apache-2.0, https://github.com/google/blockly */\n{js}\n</script>')
s = s.replace('<script>\n(function(){\n', '<script>window.__WOMBAT_MEDIA__ = ' + json.dumps(media) + ';</script>\n<script>\n(function(){\n', 1)
assert '__WOMBAT_MEDIA__ = ' in s
pathlib.Path('index.html').write_text(s, encoding='utf-8')
print('index.html', len(s.encode())//1024, 'KB')
