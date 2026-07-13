#!/usr/bin/env python3
"""
index.html을 템플릿으로 삼아 업체별 정적 명함 파일을 생성한다.
index.html의 CARDS 데이터를 수정한 뒤 이 스크립트를 실행하면
각 파일의 <title>과 기본 카드가 자동으로 갱신된다.

사용법: python3 build.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE = (ROOT / "index.html").read_text(encoding="utf-8")

# CARDS 객체에서 id: { ... name: '...' ... } 를 순서대로 추출
CARDS_BLOCK = re.search(r"const CARDS = \{(.*?)\n  \};", TEMPLATE, re.S).group(1)
CARD_IDS = re.findall(r"\n    (\w+): \{", CARDS_BLOCK)

def extract_field(card_id, field):
    card_block = re.search(rf"\n    {card_id}: \{{(.*?)\n    \}},?\n", TEMPLATE, re.S)
    m = re.search(rf"{field}: '((?:[^'\\]|\\.)*)'", card_block.group(1))
    return m.group(1) if m else ""

for card_id in CARD_IDS:
    name = extract_field(card_id, "name")
    title = f"디지털명함-{name}"
    out = TEMPLATE.replace(
        "<title>디지털명함</title>", f"<title>{title}</title>"
    ).replace(
        "const DEFAULT_ID = '';", f"const DEFAULT_ID = '{card_id}';"
    )
    (ROOT / f"{card_id}.html").write_text(out, encoding="utf-8")
    print(f"생성됨: {card_id}.html (title: {title})")
