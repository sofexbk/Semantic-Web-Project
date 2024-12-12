# Projet RDF DBPedia

Ce projet démontre l'utilisation de RDF, SPARQL et l'API DBPedia en Python.

## Installation

1. Créer un environnement virtuel Python :
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix/MacOS
# ou
venv\Scripts\activate  # Sur Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Structure du projet

- `src/config.py` : Configuration de l'endpoint DBPedia
- `src/sparql_client.py` : Client SPARQL pour interroger DBPedia
- `src/rdf_utils.py` : Utilitaires pour manipuler les données RDF
- `src/query_examples.py` : Exemples de requêtes SPARQL
- `src/main.py` : Programme principal

## Utilisation

Pour exécuter le programme :

```bash
python src/main.py
```

## Fonctionnalités

1. Interrogation de DBPedia pour obtenir :
   - Les 10 plus grandes villes françaises
   - Une liste d'écrivains français

2. Manipulation locale de graphes RDF :
   - Création de graphes
   - Ajout de triplets
   - Sauvegarde au format Turtle"# Semantic-Web-Project" 
