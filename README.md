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
