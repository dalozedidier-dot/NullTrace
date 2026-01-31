# NullTrace

Prototype v0.1 du module NullTrace.

## Installation

```
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install
```

## Lancement

```
python src/null_trace.py tests/data/current.csv --previous-shadow tests/data/previous_shadow.csv --output-dir outputs
```

## Format attendu des fichiers d’entrée

### `current.csv`

- CSV (séparateur virgule) avec en-tête.
- Colonnes : observations numériques (1..n dimensions).  
- L’outil consomme le fichier tel quel : pas de normalisation « narrative » implicite. (Si une normalisation existe, elle est celle implémentée dans le code.)

### `previous_shadow.csv`

- CSV représentant un *shadow* déjà calculé (baseline).
- Il doit correspondre au format produit par le module/outil de génération de shadow présent dans le dépôt (ex: `dd_shadow.py`).
- En pratique : si tu n’as pas de baseline, utilise le fichier fourni dans `tests/data/previous_shadow.csv` comme référence de départ.

## Objectif

Produire un shadow descriptif et un diff descriptif entre deux versions de données.
