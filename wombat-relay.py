#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
웜뱃 연결 도우미 (Wombat Relay)
Copyright (C) 2026 KISS Institute for Practical Robotics (KIPR) — https://www.kipr.org/
License: GPL-3.0-only

웜뱃 블록코딩 웹앱(wombat-blocks.html)을 이 컴퓨터의 http://localhost:8765 에서 열고,
웹앱의 요청을 Wombat(KIPR Software Suite, 포트 8888)으로 그대로 전달합니다.
브라우저 입장에서는 웹앱과 Wombat이 같은 주소가 되므로, 예전 IDE(Harrogate)처럼
다른 주소의 접속을 허용하지 않는 Wombat에도 연결할 수 있습니다.

사용법:  python3 wombat-relay.py [Wombat주소]      예) python3 wombat-relay.py 192.168.124.1
         (주소를 생략하면 192.168.124.1, 웹앱의 [Wombat 연결] 창에서 바꿀 수도 있습니다)
종료:    이 창에서 Control+C
외부 패키지가 필요 없습니다 (Python 3.7 이상 표준 라이브러리만 사용).
"""
import http.client
import http.server
import json
import os
import re
import sys
import threading
import webbrowser
from pathlib import Path

PORT = int(os.environ.get('WOMBAT_RELAY_PORT', '8765'))
HERE = Path(__file__).resolve().parent
APP_FILES = [HERE / 'wombat-blocks.html', HERE / 'index.html']
HOP = {'connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization', 'te', 'trailers',
       'transfer-encoding', 'upgrade', 'host', 'origin', 'referer', 'accept-encoding'}
HOST_RE = re.compile(r'^[A-Za-z0-9.\-]{1,253}$')

target = {'host': '192.168.124.1', 'port': 8888}
if len(sys.argv) > 1:
    h, _, p = sys.argv[1].partition(':')
    if HOST_RE.match(h):
        target['host'] = h
        if p.isdigit():
            target['port'] = int(p)


def app_file():
    for f in APP_FILES:
        if f.exists():
            return f
    return None


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    server_version = 'WombatRelay/1.0'

    def log_message(self, fmt, *args):  # 조용히 (오류만 출력)
        pass

    def _send(self, code, body, ctype='application/json; charset=utf-8'):
        data = body if isinstance(body, bytes) else body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)

    def _relay_info(self):
        return json.dumps({'relay': True, 'target': f"{target['host']}:{target['port']}"})

    # ---- 라우팅 ----
    def do_GET(self):
        path = self.path.split('?')[0]
        if path in ('/', '/index.html', '/wombat-blocks.html'):
            f = app_file()
            if not f:
                return self._send(404, '<h1>wombat-blocks.html 파일이 이 프로그램과 같은 폴더에 없습니다.</h1>', 'text/html; charset=utf-8')
            return self._send(200, f.read_bytes(), 'text/html; charset=utf-8')
        if path == '/__relay':
            return self._send(200, self._relay_info())
        if path == '/favicon.ico':
            return self._send(204, b'', 'image/x-icon')
        self._proxy()

    def do_POST(self):
        if self.path.split('?')[0] == '/__relay':
            try:
                body = json.loads(self.rfile.read(int(self.headers.get('Content-Length') or 0)) or b'{}')
                h, _, p = str(body.get('target', '')).partition(':')
                if not HOST_RE.match(h):
                    return self._send(400, json.dumps({'error': '주소 형식이 올바르지 않습니다'}))
                target['host'] = h
                target['port'] = int(p) if p.isdigit() else 8888
                print(f"  → 연결 대상 변경: {target['host']}:{target['port']}", flush=True)
                return self._send(200, self._relay_info())
            except Exception as e:  # noqa
                return self._send(400, json.dumps({'error': str(e)}))
        self._proxy()

    do_PUT = do_DELETE = do_PATCH = do_OPTIONS = lambda self: self._proxy()

    # ---- Wombat으로 전달 ----
    def _proxy(self):
        length = int(self.headers.get('Content-Length') or 0)
        body = self.rfile.read(length) if length else None
        headers = {k: v for k, v in self.headers.items() if k.lower() not in HOP}
        headers['Host'] = f"{target['host']}:{target['port']}"
        # 실행 출력처럼 오래 열려 있는 요청도 있으므로 넉넉한 시간 제한
        conn = http.client.HTTPConnection(target['host'], target['port'], timeout=120)
        try:
            conn.request(self.command, self.path, body=body, headers=headers)
            resp = conn.getresponse()
        except OSError as e:
            conn.close()
            return self._send(502, json.dumps({
                'relay_error': True,
                'error': f"Wombat({target['host']}:{target['port']})에 연결할 수 없습니다: {e}"}, ensure_ascii=False))
        try:
            self.send_response(resp.status, resp.reason)
            has_len = False
            for k, v in resp.getheaders():
                kl = k.lower()
                if kl in HOP:
                    continue
                if kl == 'content-length':
                    has_len = True
                self.send_header(k, v)
            if not has_len:
                # 길이를 모르는 응답(실행 출력 스트림 등)은 다 보낸 뒤 연결을 닫는다
                self.send_header('Connection', 'close')
                self.close_connection = True
            self.end_headers()
            while True:
                chunk = resp.read1(8192) if hasattr(resp, 'read1') else resp.read(8192)
                if not chunk:
                    break
                self.wfile.write(chunk)
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            self.close_connection = True
        finally:
            conn.close()


class QuietServer(http.server.ThreadingHTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        # 브라우저가 연결을 먼저 끊는 것은 정상 동작이므로 조용히 넘어감
        if isinstance(sys.exc_info()[1], (ConnectionResetError, BrokenPipeError, ConnectionAbortedError, TimeoutError)):
            return
        super().handle_error(request, client_address)


def main():
    if not app_file():
        print('⚠️  wombat-blocks.html 파일을 이 프로그램과 같은 폴더에 두세요.')
    try:
        server = QuietServer(('127.0.0.1', PORT), Handler)
    except OSError:
        # 이미 켜진 도우미가 정상인지(응답하는지) 확인
        alive = False
        try:
            c = http.client.HTTPConnection('127.0.0.1', PORT, timeout=2)
            c.request('GET', '/__relay')
            alive = c.getresponse().status == 200
            c.close()
        except OSError:
            pass
        if alive:
            print(f'ℹ️  연결 도우미가 이미 켜져 있습니다. 브라우저에서 http://localhost:{PORT} 을 여세요.')
            webbrowser.open(f'http://localhost:{PORT}/')
        else:
            print(f'⚠️  포트 {PORT}을(를) 다른 프로그램(또는 Control+Z로 멈춘 도우미)이 쓰고 있습니다.')
            print('    아래 명령으로 끈 뒤 다시 실행하세요:')
            if os.name == 'nt':
                print(f'      for /f "tokens=5" %a in (\'netstat -ano ^| findstr :{PORT}\') do taskkill /F /PID %a')
            else:
                print('      pkill -9 -f wombat-relay.py')
        return
    url = f'http://localhost:{PORT}/'
    print('=' * 60)
    print(' 🤖 웜뱃 연결 도우미가 켜졌습니다')
    print(f'    웹앱 주소 : {url}')
    print(f"    Wombat    : {target['host']}:{target['port']} (웹앱의 [Wombat 연결]에서 변경 가능)")
    print('    끝내려면 이 창에서 Control+C 를 누르세요. (창을 닫아도 됩니다)')
    print('=' * 60, flush=True)
    if os.environ.get('WOMBAT_RELAY_NO_BROWSER') != '1':
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n연결 도우미를 종료합니다.')


if __name__ == '__main__':
    main()
