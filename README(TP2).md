README - Inverted Index pour Produits
Description
Ce script crée des index inversés pour les titres, descriptions, avis et caractéristiques des produits à partir d'un fichier JSONL.

Index Créés
Index des Titres et Descriptions :
Indexe chaque mot avec l'URL du produit et sa position.

Index des Avis :
Contient le nombre d'avis, la moyenne et la dernière note des produits.

Index des Caractéristiques :
Indexe les caractéristiques (marque, origine, etc.) avec les produits associés.

Choix Techniques
Tokenisation et stopwords : Filtrage des mots non significatifs.
Index inversé : Optimisation des recherches par mot-clé.
Calcul des statistiques : Nombre d'avis, moyenne, dernière note.
Utilisation
Prérequis : Python 3.x

Exécution :

bash
Copier
python script.py
Les index sont sauvegardés dans des fichiers JSON.
