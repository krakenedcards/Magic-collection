#!/usr/bin/env python3
"""Add a card to the collection from a Scryfall URL or exact card name."""

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "collection" / "cards.json"
API = "https://api.scryfall.com"

def fetch_card(query: str) -> dict:
    if query.startswith("https://scryfall.com/card/"):
        path = urllib.parse.urlsplit(query).path.strip("/").split("/")
        if len(path) >= 3:
            url = f"{API}/cards/{urllib.parse.quote(path[1])}/{urllib.parse.quote(path[2])}"
        else:
            raise SystemExit("Invalid Scryfall card URL.")
    else:
        url = f"{API}/cards/named?exact={urllib.parse.quote(query)}"

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Magic-collection/1.0"}
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)

def face_data(face: dict) -> dict:
    keys = ("name", "mana_cost", "type_line", "oracle_text", "colors",
            "power", "toughness", "loyalty")
    return {key: face[key] for key in keys if key in face}

def normalize(card: dict) -> dict:
    result = {
        "oracle_id": card["oracle_id"],
        "name": card["name"],
        "scryfall_uri": card["scryfall_uri"],
        "mana_cost": card.get("mana_cost", ""),
        "cmc": card.get("cmc", 0),
        "type_line": card.get("type_line", ""),
        "colors": card.get("colors", []),
        "color_identity": card.get("color_identity", []),
        "oracle_text": card.get("oracle_text", ""),
        "keywords": card.get("keywords", []),
        "legalities": card.get("legalities", {}),
        "owned": True,
    }
    for key in ("power", "toughness", "loyalty", "defense", "produced_mana"):
        if key in card:
            result[key] = card[key]
    if "card_faces" in card:
        result["card_faces"] = [face_data(face) for face in card["card_faces"]]
    return result

def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 scripts/add_scryfall.py '<Scryfall URL or exact card name>'")

    data = json.loads(DATA.read_text(encoding="utf-8"))
    card = normalize(fetch_card(sys.argv[1]))
    cards = [c for c in data["cards"] if c["oracle_id"] != card["oracle_id"]]
    cards.append(card)
    cards.sort(key=lambda c: c["name"].lower())
    data["cards"] = cards
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added/updated: {card['name']} ({card['oracle_id']})")

if __name__ == "__main__":
    main()
