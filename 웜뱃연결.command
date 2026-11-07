#!/bin/bash
# 웜뱃 연결 도우미 실행 (Mac) — 더블클릭하세요
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3가 없습니다. 터미널에서 'xcode-select --install'로 설치한 뒤 다시 실행하세요."
  read -n 1 -s -r -p "아무 키나 누르면 닫힙니다."
  exit 1
fi
python3 wombat-relay.py "$@"
