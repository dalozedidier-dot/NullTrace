# NullTrace

Prototype v0.1 du module NullTrace.

## Installation
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install

## Lancement
python src/null_trace.py tests/data/current.csv --previous-shadow tests/data/previous_shadow.csv --output-dir outputs

## Objectif
Produire un shadow descriptif et un diff descriptif entre deux versions de données.

## Format attendu (current.csv / previous_shadow.csv)
- CSV UTF-8 avec en-tête.
- Colonnes: au minimum une ou plusieurs colonnes numériques (les colonnes non numériques sont ignorées si elles ne sont pas comparées).
- Les deux fichiers doivent partager un sous-ensemble de colonnes communes ; la comparaison s'effectue sur l'intersection.
- Ordre des lignes: supposé stable. Si l'ordre varie, fournir une clé d'alignement (à implémenter si nécessaire).
