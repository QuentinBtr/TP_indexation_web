# Web Crawler Python

Un simple crawler web qui explore les sites en respectant robots.txt et sauvegarde les données en JSON.

## Installation

```bash
pip install beautifulsoup4
```

## Comment l'utiliser

1. Créez un fichier Python avec le code du crawler
2. Exécutez le avec :
```python
from web_crawler import WebCrawler

crawler = WebCrawler("https://votre-site.com", max_pages=50)
crawler.run()
```

## Fonctionnement

- Explore les pages web automatiquement
- Limite à 50 pages par défaut
- Priorité aux pages contenant "product" dans l'URL
- Sauvegarde les résultats dans results.json
- Respecte un délai de 1 seconde entre chaque page

## Résultat

Crée un fichier results.json contenant :
- Titre de la page
- URL
- Premier paragraphe
- Liste des liens trouvés
- Date et heure du crawl

## Notes
- Fonctionne uniquement avec Python 3.x
- Nécessite une connexion internet
- Ne crawle que les liens internes au site de départ
