// Mock of KIPR Harrogate 1.0.1 (old Wombat IDE) — NO CORS headers, socket.io 1.4.8 '/runner' namespace.
// Usage: node server.js [port]   (default 8898)
const express = require('express'), bodyParser = require('body-parser'), http = require('http');
const fs = require('fs'), path = require('path'), { spawn, exec } = require('child_process');
const PORT = +process.argv[2] || 8898;
const WS = path.join(__dirname, 'ws');           // workspace root (like /home/kipr/Documents/KISS)
const STUB = path.join(__dirname, '..', 'mock', 'stub');
const users = { 'Default User': { mode: 'Simple' }, '학생1': { mode: 'Simple' } };
const seed = [['학생1', '블록코딩', 'Python'], ['학생1', 'c_proj', 'C'], ['Default User', '빈프로젝트', 'Python']];
for (const [u, p, lang] of seed) {
  const d = path.join(WS, u, p); fs.mkdirSync(path.join(d, 'src'), { recursive: true }); fs.mkdirSync(path.join(d, 'bin'), { recursive: true });
  fs.writeFileSync(path.join(d, 'project.manifest'), JSON.stringify({ language: lang, user: u }));
  if (p === '블록코딩') fs.writeFileSync(path.join(d, 'src', 'main.py'), 'print("old")\n');
}
const uri = p => '/api/fs' + p;
const app = express(); app.use(bodyParser.json({ limit: '5mb' }));
const log = []; app.use((q, r, n) => { log.push(q.method + ' ' + decodeURI(q.path)); fs.writeFileSync(path.join(__dirname, 'requests.log'), log.join('\n')); n(); });

app.get('/api/projects/users', (q, r) => r.json(users));
app.get('/api/projects/:user', (q, r) => {
  const ud = path.join(WS, q.params.user);
  if (!fs.existsSync(ud)) return r.json({ projects: [] });
  const projects = fs.readdirSync(ud).map(name => {
    const d = path.join(ud, name), params = JSON.parse(fs.readFileSync(path.join(d, 'project.manifest'), 'utf8'));
    const src = path.join(d, 'src');
    return { name, parameters: params, links: { src_directory: { href: uri(src) }, bin_directory: { href: uri(path.join(d, 'bin')) } },
      source_files: fs.readdirSync(src).map(f => ({ name: f, path: path.join(src, f), links: { self: { href: uri(path.join(src, f)) } } })) };
  });
  r.set('Content-Type', 'application/javascript').send(JSON.stringify({ projects }));
});
const fsPath = q => decodeURI(q.originalUrl.split('?')[0]).slice('/api/fs'.length);
app.put('/api/fs/*', (q, r) => {
  if (!/application\/json/i.test(q.headers['content-type'] || '')) return r.status(415).end();
  const p = fsPath(q); if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) return r.status(400).json({ error: p + ' is not a file' });
  fs.writeFileSync(p, Buffer.from(q.body.content || '', 'base64').toString(q.body.encoding || 'ascii'), q.body.encoding || 'ascii'); r.status(204).end();
});
app.post('/api/fs/*', (q, r) => {
  const p = fsPath(q); if (!fs.existsSync(p) || !fs.statSync(p).isDirectory()) return r.status(400).json({ error: 'not a directory' });
  const f = path.join(p, q.body.name); fs.writeFileSync(f, Buffer.from(q.body.content || '', 'base64').toString(q.body.encoding || 'ascii'));
  r.status(201).set('Location', encodeURI(uri(f))).end();
});
const findProject = (u, n) => { const d = path.join(WS, u || '', n || ''); return fs.existsSync(path.join(d, 'project.manifest')) ? d : null; };
app.post('/api/compile', (q, r) => {
  const d = findProject(q.body.user, q.body.name); if (!d) return r.status(404).json({ error: 'Project ' + q.body.name + ' does not exists' });
  const bin = path.join(d, 'bin'); fs.rmSync(bin, { recursive: true, force: true }); fs.mkdirSync(bin);
  for (const f of fs.readdirSync(path.join(d, 'src'))) fs.copyFileSync(path.join(d, 'src', f), path.join(bin, f));
  exec(`python3 -m py_compile "${path.join(bin, 'main.py')}"`, (error, stdout, stderr) => r.json({ result: { stdout, stderr, error } }));
});
let child = null;
const http_ = http.createServer(app); const io = require('socket.io')(http_); const ns = io.of('/runner');
app.post('/api/run', (q, r) => {
  const d = findProject(q.body.user, q.body.name); if (!d) return r.status(404).json({ error: 'not found' });
  if (child) return r.status(409).json({ error: q.body.name + ' is already running' });
  ns.emit('starting', q.body.name);
  child = spawn('python3', [path.join(d, 'bin', 'main.py')], { env: { ...process.env, PYTHONPATH: STUB } });
  child.stdout.on('data', x => ns.emit('stdout', x.toString('utf8')));
  child.stderr.on('data', x => ns.emit('stderr', x.toString('utf8')));
  child.on('exit', code => { ns.emit('stdout', 'Program exited with code ' + code); ns.emit('ended'); child = null; });
  r.status(201).json({ running: { name: q.body.name } });
});
app.delete('/api/run/current', (q, r) => { if (child) child.kill('SIGINT'); r.json({ running: null }); });
app.use(express.static(path.join(__dirname, 'public')));
http_.listen(PORT, '127.0.0.1', () => console.log('mock harrogate on ' + PORT));
