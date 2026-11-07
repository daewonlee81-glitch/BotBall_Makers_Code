# 웜뱃 블록코딩 (Wombat Blocks)

KIPR **Wombat** 로봇을 크롬에서 **한글 블록**으로 코딩하는 웹앱입니다.
왼쪽에서 블록을 조립하면 오른쪽에 **Python 코드**가 바로 만들어지고, Wombat으로 보내 **실행·정지**까지 할 수 있습니다.

- 파일 하나(`index.html`)로 동작하며, 라이브러리를 모두 담고 있어 **인터넷 없이도** 열립니다.
- 생성 코드는 KIPR Software Suite의 Python 템플릿(`from kipr import *`)을 따릅니다.

## 주요 기능

- **한글 블록**: 시작(봇볼), 모터, 서보, 센서, 버튼, 시간, 화면·소리, 카메라, Create 3, Create(구형) + 논리·반복·수학·텍스트·변수·함수
- **Python 코드 실시간 생성**: 한글 변수·함수 이름 그대로 사용, KIPR 정수 인자 자동 `int()` 처리, `print(..., flush=True)`
- **Wombat 직접 연결**: 코드 저장 → 문법 검사 → 실행(출력 실시간 표시) → 정지(모든 모터 끄기)
- 예제 7종, 프로젝트 `.json` 저장/불러오기, 브라우저 자동 저장, 코드 복사, `.py` 내려받기

## 사용 방법

1. `index.html`을 크롬에서 엽니다. (더블클릭)
2. 블록을 조립하고 **코드 복사**로 KIPR Software Suite에 붙여넣거나, 아래처럼 바로 실행합니다.

### Wombat에 바로 보내 실행하기

1. 처음 한 번, 크롬에서 `Wombat 주소:8888`로 **KIPR Software Suite**를 열고 사용자를 만든 뒤 언어를 **Python**으로 골라 프로젝트를 만듭니다.
2. 웹앱 상단 **Wombat 연결** → 주소 선택 → **연결 확인** → 사용자·Python 프로젝트 선택 → **이 프로젝트로 연결**.
3. **▶ 실행**(Ctrl+Enter) / **■ 정지**.

> ⚠️ 연결한 프로젝트의 `src/main.py`는 웹앱 코드로 **덮어써집니다.** 블록코딩용 프로젝트를 따로 만들어 쓰세요.
> 최신 WombatOS(IDE: Voldigate) 기준입니다. 예전 펌웨어(harrogate)에서는 동작하지 않습니다.

### 연결 방법

| 방법 | 주소 | 비고 |
|---|---|---|
| Wi‑Fi | `192.168.125.1` (About의 WiFi 줄) | Wombat Wi‑Fi에는 인터넷이 없음 |
| 랜선 직접 연결 | `192.168.124.1` (About의 LAN 줄) | About에서 **Event Mode**를 먼저 켬, 1대 1 연결 |

**인터넷을 쓰면서 제어하기**: Wombat은 랜선, 인터넷은 학교 Wi‑Fi로 연결하고, 컴퓨터의 유선 랜 IP를 **수동**으로
`192.168.124.10` / `255.255.255.0`, **게이트웨이는 비워 두세요.** (Wombat이 자신을 게이트웨이로 알려 주기 때문)

### 웹 호스팅(GitHub Pages 등) 주의

https로 호스팅한 페이지는 브라우저 보안 정책(혼합 콘텐츠) 때문에 http인 Wombat에 접속할 수 없습니다.
블록 코딩·코드 복사는 호스팅된 페이지에서도 되지만, **직접 실행은 `index.html`을 내려받아 로컬에서 열어야** 합니다.

## 폴더 구조

```
app.src.html   웹앱 원본 (블록 정의, Python 생성기, UI, Wombat 연결)
build.py       app.src.html + Blockly → index.html (라이브러리·아이콘 내장)
index.html     빌드 결과물 (배포용 단일 파일)
test/          자동 테스트 (Playwright)
mock/          Wombat IDE(Voldigate) 모의 서버 + KIPR 라이브러리 스텁
```

## 빌드

```bash
npm install          # blockly 13.4.0
python3 build.py     # → index.html
```

`index.html`은 직접 고치지 말고 `app.src.html`을 고친 뒤 다시 빌드하세요.

## 테스트

```bash
pip install playwright && playwright install chromium   # 또는 CHROME_PATH=/path/to/chrome
python3 test/run.py && python3 test/check.py test/kipr_names.txt test/codes.json   # 예제·전체 블록 코드 생성 + 문법·함수명 검사
python3 test/var.py                                     # 한글 변수·함수 이름 검사
node mock/server.js &                                   # 모의 Wombat (127.0.0.1:8899)
python3 test/e2e.py                                     # 연결·실행·정지·문법오류 표시
python3 test/offline.py                                 # 인터넷 차단 상태에서 로딩
```

## 사용한 Wombat IDE API (Voldigate, 포트 8888)

| 기능 | 요청 |
|---|---|
| 사용자 목록 | `GET /get-users` |
| 프로젝트 목록 | `GET /get-projects?userName=` |
| 코드 저장 | `POST /save-file-content` `{filePath, fileContents}` |
| 문법 검사 | `POST /compile-code` `{userName, projectName, fileName, activeLanguage}` |
| 실행(스트림) | `GET /run-code?userName&projectName&fileName&activeLanguage=python` |
| 정지 | `POST /stop-code` |

## 현재 상태

- 모의 서버와 헤드리스 크롬으로 검증했습니다. **실제 Wombat 실기 테스트는 진행 전**입니다.
- Create 3 블록은 Wombat 펌웨어의 Python 바인딩 지원 여부를 실기로 확인해야 합니다.

## 참고 자료

- KIPR libkipr 문서: https://www.kipr.org/doc/index.html
- KIPR Writing Your First Program: https://www.kipr.org/wp-content/uploads/2025/08/Writing_Your_First_Program.pdf
- kipr/voldigate (Wombat IDE): https://github.com/kipr/voldigate
- kipr/wombat-os: https://github.com/kipr/wombat-os

## 라이선스

Copyright (C) 2026 KISS Institute for Practical Robotics (KIPR) — https://www.kipr.org/

이 프로젝트는 KIPR의 Wombat 소프트웨어(libkipr, KIPR Simulator, Voldigate, Wombat OS)와 같은
**GNU General Public License v3.0 (GPL-3.0-only)** 로 배포됩니다. 전문은 [`LICENSE`](LICENSE), 고지 사항은 [`NOTICE`](NOTICE)를 보세요.

- `index.html`에 포함된 [Blockly](https://github.com/google/blockly)(Google LLC)는 Apache License 2.0을 따릅니다.
- BOTBALL®, BOTGUY™ 및 관련 디자인은 KISS Institute for Practical Robotics의 상표입니다.
