# 브랜드 이미지 (이 프로젝트 전용)

웜뱃 블록코딩 웹앱에서만 사용하는 Botball 로고와 아이콘입니다.

| 파일 | 용도 |
|---|---|
| `botball-logo.jpg` | 원본 Botball 로고 |
| `botguy.png` | 로고에서 Botguy만 잘라낸 투명 배경 이미지 |
| `favicon-32.png`, `favicon-64.png` | 브라우저 탭 아이콘 |
| `apple-touch-icon.png` (180×180) | iPhone·iPad 홈 화면 아이콘 |
| `icon-192.png`, `icon-512.png` | 바로가기·앱 아이콘 |
| `header-badge.png` | 웹앱 상단 로고 |
| `og-image.png` (1200×630) | 링크 공유 미리보기 섬네일 |
| `make_icons.py` | 원본 로고에서 위 이미지를 다시 만드는 스크립트 |

- 빌드(`python3 build.py`) 때 탭 아이콘·홈 화면 아이콘·상단 로고는 `index.html` 안에 내장되므로,
  웹앱은 이 폴더 없이도 파일 하나로 동작합니다. 링크 미리보기(`og-image.png`)만 이 폴더를 참조합니다.
- 로고를 바꾸려면 `botball-logo.jpg`를 교체하고 `python3 make_icons.py` → `python3 build.py`를 실행하세요.

> BOTBALL®, BOTGUY™ 및 BOTGUY™ 디자인·캐릭터는 KISS Institute for Practical Robotics(KIPR)의 상표입니다.
> 이 폴더의 이미지는 이 프로젝트에서만 사용하며, 다른 용도로 쓰려면 KIPR의 사전 서면 허락이 필요합니다.
