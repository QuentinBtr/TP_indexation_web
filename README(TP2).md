# Indexeur de Produits

## Description
Script Python pour l'indexation complète de données de produits à partir d'un fichier JSONL, créant plusieurs index spécialisés pour une recherche et une analyse efficaces.

## Fonctionnalités
- Extraction des ID et variantes de produits depuis des URLs
- Création d'index inversés pour les titres et descriptions
- Génération de statistiques sur les avis
- Construction d'index basés sur les caractéristiques
- Suppression des mots-vides et normalisation du texte
- Sauvegarde des index au format JSON

## Prérequis
- Python 3.7+
- Modules de la bibliothèque standard : `json`, `re`, `typing`, `statistics`, `datetime`, `collections`

## Utilisation
1. Préparer un fichier JSONL avec les données de produits
2. Exécuter le script pour générer les index

```bash
python product_indexer.py
```

## Index Générés
- Index des Titres : Tokens recherchables des titres
- Index des Descriptions : Tokens recherchables des descriptions
- Index des Avis : Statistiques des avis produits
- Index des Caractéristiques : Caractéristiques des produits par catégorie

## Fonctions Principales
- `load_jsonl()` : Charger et analyser les données de produits
- `create_title_and_description_indexes()` : Créer des index de texte recherchables
- `create_reviews_index()` : Agréger les statistiques d'avis
- `create_features_indexes()` : Indexer les caractéristiques des produits

## Fichiers de Sortie
- `title_index.json`
- `description_index.json`
- `reviews_index.json`
- `features_indexes.json`

## Remarques
- Mots-vides supprimés lors de l'indexation
- Index utilisant les URLs de produits comme identifiants
- Prise en charge du traitement de texte multilingue
