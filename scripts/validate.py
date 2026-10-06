#!/usr/bin/env python3
"""Validate the Magic collection JSON without external dependencies."""

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "collection" / "cards.json"

def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)

try:
    data = json.loads(DATA.read_text(encoding="utf-8"))
except Exception as exc:
    fail(f"cannot read {DATA}: {exc}")

if data.get("version") != 1:
    fail("unsupported or missing collection version")

cards = data.get("cards")
if not isinstance(cards, list):
    fail("'cards' must be an array")

seen = set()
for index, card in enumerate(cards):
    if not isinstance(card, dict):
        fail(f"cards[{index}] must be an object")

    required = [
        "oracle_id", "name", "scryfall_uri", "mana_cost", "cmc",
        "type_line", "colors", "color_identity", "oracle_text",
        "keywords", "legalities", "owned"
    ]
    missing = [key for key in required if key not in card]
    if missing:
        fail(f"cards[{index}] missing: {', '.join(missing)}")

    oracle_id = card["oracle_id"]
    if oracle_id in seen:
        fail(f"duplicate oracle_id: {oracle_id}")
    seen.add(oracle_id)

    if not isinstance(oracle_id, str) or not oracle_id:
        fail(f"cards[{index}].oracle_id must be a non-empty string")

    if not re.match(r"^https://scryfall\\.com/", card["scryfall_uri"]):
        fail(f"cards[{index}].scryfall_uri must be a Scryfall URL")

    if card["owned"] is not True:
        fail(f"cards[{index}].owned must be true for a collection entry")

print(f"OK: {len(cards)} unique cards")
