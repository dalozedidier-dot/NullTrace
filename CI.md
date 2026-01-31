# CI commune (GitHub Actions)

Ce dépôt utilise un workflow CI unique, identique sur les 4 repos (RiftLens, NullTrace, VoidMark, BareFlux).

## Où sont les "rapports" ?
GitHub Actions ne commit rien automatiquement dans le repo.
Les rapports sont visibles **dans l’onglet Actions** du repo, run par run.

Dans ce workflow, deux fichiers sont **uploadés comme artifacts** :
- `coverage.xml`
- `pytest-junit.xml`

Tu les retrouves en bas de la page d’un run (section **Artifacts**).

## Ajout du fichier
Chemin à créer dans le repo :
`.github/workflows/ci.yml`

Copie-colle le contenu du fichier `ci.yml` fourni (CI – Tests, Lint & Coverage).

## Activation
1. Push sur `main` (ou `master`) ou PR vers `main/master`.
2. Va dans l’onglet **Actions**.
3. Ouvre le run **CI – Tests, Lint & Coverage**.

## Vérification
- Matrice Python 3.10 / 3.11 / 3.12
- pre-commit exécuté (non bloquant)
- pytest + coverage (seuil 70 % dans la commande)
- artifacts disponibles : `coverage.xml`, `pytest-junit.xml`
- Codecov optionnel si `CODECOV_TOKEN` est défini (Settings → Secrets → Actions)
