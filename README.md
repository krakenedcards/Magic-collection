# Magic Collection

Collection personnelle de cartes Magic: The Gathering.

## Principes

- Une carte est identifiée par son **oracle_id** Scryfall, pas par son édition, sa langue ou son numéro de collection.
- La collection indique seulement si au moins un exemplaire est possédé.
- Chaque carte possède son lien Scryfall dans `scryfall_uri`.
- Les informations de jeu utiles sont conservées pour permettre des recherches ultérieures : nom, mana cost, types, couleurs, identité couleur, texte Oracle, mots-clés, force/endurance, loyauté, légalité, etc.
- Le nombre d'exemplaires, la langue, le traitement foil/non-foil et l'édition possédée ne sont volontairement pas des critères d'identité.

## Structure

```text
collection/
  cards.json          # Cartes possédées, une entrée par oracle_id
  schema.json         # Contrat de données
scripts/
  validate.py         # Validation locale de la collection
```

## Ajouter une carte

Ajouter ou mettre à jour une entrée dans `collection/cards.json` avec les données Scryfall correspondantes.

Exemple :

```json
{
  "oracle_id": "…",
  "name": "Lightning Bolt",
  "scryfall_uri": "https://scryfall.com/card/…",
  "mana_cost": "{R}",
  "cmc": 1,
  "type_line": "Instant",
  "colors": ["R"],
  "color_identity": ["R"],
  "oracle_text": "Lightning Bolt deals 3 damage to any target.",
  "keywords": [],
  "legalities": {},
  "owned": true
}
```

Le champ `owned` est explicite afin que les données restent extensibles, mais une entrée présente dans `collection/cards.json` représente par convention une carte possédée.

## Validation

```bash
python3 scripts/validate.py
```

La source de vérité des données de carte est Scryfall.
