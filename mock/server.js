// Mock of KIPR Voldigate (Wombat IDE) — same CORS middleware + catch-all as express.js
const http=require('http'),fs=require('fs'),path=require('path'),{spawn,execFileSync}=require('child_process');
const ROOT='/home/kipr/Documents/KISS', TMP=path.join(__dirname,'kiss');
const users={'학생1':{userName:'학생1',projects:[{projectName:'블록코딩',projectLanguage:'python'},{projectName:'c_proj',projectLanguage:'c'}]},'teacher':{userName:'teacher',projects:[]}};
let child=null; const log=[];
const local=p=>path.join(TMP,path.relative(ROOT,p));
http.createServer((req,res)=>{
  res.setHeader('Access-Control-Allow-Origin','*');
  res.setHeader('Access-Control-Allow-Headers','Origin, X-Requested-With, Content-Type, Accept');
  const u=new URL(req.url,'http://x'); let body='';
  req.on('data',d=>body+=d); req.on('end',()=>{
    log.push(req.method+' '+u.pathname); fs.writeFileSync(path.join(__dirname,'requests.log'),log.join('\n'));
    const json=(o,s=200)=>{res.writeHead(s,{'Content-Type':'application/json'});res.end(JSON.stringify(o));};
    let b={}; try{b=JSON.parse(body||'{}')}catch(e){}
    if(req.method==='GET'&&u.pathname==='/get-users') return json({users:Object.values(users).map(x=>({userName:x.userName,interfaceMode:'Simple'}))});
    if(req.method==='GET'&&u.pathname==='/get-projects'){const x=users[u.searchParams.get('userName')]; return x?json({projects:x.projects}):json({error:'User not found'},404);}
    if(req.method==='POST'&&u.pathname==='/save-file-content'){ if(!b.filePath||!b.fileContents) return json({error:'Missing'},400); const p=local(b.filePath); fs.mkdirSync(path.dirname(p),{recursive:true}); fs.writeFileSync(p,b.fileContents); res.end('File saved successfully'); return;}
    if(req.method==='POST'&&u.pathname==='/compile-code'){ const p=path.join(TMP,b.userName,b.projectName,'src','main.py'); try{execFileSync('python3',['-m','py_compile',p],{encoding:'utf8',stdio:'pipe'}); return json({message:'successful',error:null,warnings:[],messages:[]});}catch(e){return json({message:'failed',error:e.stderr||e.message});}}
    if(req.method==='GET'&&u.pathname==='/run-code'){ const p=path.join(TMP,u.searchParams.get('userName'),u.searchParams.get('projectName'),'src','main.py');
      res.writeHead(200,{'Content-Type':'text/event-stream','Cache-Control':'no-cache','Connection':'keep-alive'});
      child=spawn('python3',[p],{env:{...process.env,PYTHONPATH:path.join(__dirname,'stub')},detached:true});
      res.write('data: [core/wombat] init\n\n');
      child.stdout.on('data',d=>d.toString().split('\n').forEach(l=>{if(l.trim())res.write(`data: ${l}\n\n`)}));
      child.stderr.on('data',d=>res.write(`data: ERROR: ${d.toString()}\n\n`));
      child.on('close',code=>{child=null;res.write(`data: Process exited with code ${code}\n\n`);res.write('event: end\ndata: END\n\n');res.end();});
      return;}
    if(req.method==='POST'&&u.pathname==='/stop-code'){ if(child){try{process.kill(-child.pid,'SIGKILL')}catch(e){} child=null; res.end('Execution stopped');} else {res.writeHead(400);res.end('No process running');} return;}
    res.writeHead(200,{'Content-Type':'text/html'}); res.end('<html>index</html>'); // catch-all like Voldigate (also answers OPTIONS)
  });
}).listen(8899,'127.0.0.1',()=>console.log('mock on 8899'));
