import urllib.robotparser
from urllib.request import urlopen, Request
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import json
import time
from queue import PriorityQueue
from datetime import datetime

class WebCrawler:
    def __init__(self, start_url, max_pages=50):
        """
        Initialise le crawler avec une URL de départ et un nombre maximum de pages.
        
        Args:
            start_url (str): L'URL de départ pour le crawling
            max_pages (int): Nombre maximum de pages à crawler (défaut: 50)
        """
        self.start_url = start_url
        self.base_domain = urlparse(start_url).netloc
        self.max_pages = max_pages
        self.visited = set()
        self.queue = PriorityQueue()
        self.results = []
        self.delay = 1  # Délai entre les requêtes
        self.start_time = None
        self.metrics = {
            "pages_crawled": 0,
            "total_time": 0,
            "errors": 0
        }

    def _can_fetch(self, url):
        """
        Vérifie si le crawling est autorisé selon robots.txt.
        
        Args:
            url (str): L'URL à vérifier
            
        Returns:
            bool: True si le crawling est autorisé, False sinon
        """
        rp = urllib.robotparser.RobotFileParser()
        robots_url = urljoin(url, '/robots.txt')
        try:
            rp.set_url(robots_url)
            rp.read()
            return rp.can_fetch("*", url)
        except Exception as e:
            print(f"Erreur lors de la lecture de robots.txt pour {url}: {e}")
            return False  # En cas d'erreur, on est prudent

    def _is_internal_link(self, url):
        """
        Vérifie si l'URL appartient au même domaine.
        
        Args:
            url (str): L'URL à vérifier
            
        Returns:
            bool: True si l'URL est interne, False sinon
        """
        try:
            parsed_url = urlparse(url)
            return parsed_url.netloc == self.base_domain
        except:
            return False

    def _get_html(self, url):
        """
        Récupère le HTML d'une page avec gestion des erreurs.
        
        Args:
            url (str): L'URL à récupérer
            
        Returns:
            str|None: Le contenu HTML ou None en cas d'erreur
        """
        try:
            req = Request(url, headers={"User-Agent": "PythonCrawlerBot/1.0"})
            with urlopen(req, timeout=10) as response:
                if response.status != 200:
                    print(f"Statut HTTP non-200 pour {url}: {response.status}")
                    return None
                try:
                    return response.read().decode("utf-8")
                except UnicodeDecodeError:
                    return response.read().decode("latin-1")
        except Exception as e:
            print(f"Erreur sur {url}: {e}")
            self.metrics["errors"] += 1
            return None

    def _extract_content(self, html, source_url):
        """
        Extrait le contenu avec BeautifulSoup.
        
        Args:
            html (str): Le contenu HTML à parser
            source_url (str): L'URL source pour la résolution des liens relatifs
            
        Returns:
            tuple: (titre, premier paragraphe, liste des liens)
        """
        soup = BeautifulSoup(html, "html.parser")
        
        # Extraction du titre
        title = soup.title.string.strip() if soup.title else ""
        
        # Extraction du premier paragraphe
        first_paragraph = ""
        p_tag = soup.find("p")
        if p_tag:
            first_paragraph = p_tag.get_text().strip()
        
        # Extraction des liens
        links = []
        for link in soup.find_all("a", href=True):
            try:
                absolute_url = urljoin(source_url, link["href"])
                if self._is_internal_link(absolute_url):
                    links.append(absolute_url)
            except Exception as e:
                print(f"Erreur lors de l'extraction du lien: {e}")
                continue
                
        return title, first_paragraph, links

    def _add_to_queue(self, links):
        """
        Priorise les URLs et les ajoute à la file d'attente.
        
        Args:
            links (list): Liste des URLs à ajouter
        """
        for link in links:
            if link not in self.visited and link not in {url for _, url in self.queue.queue}:
                # Priorité plus haute (0) pour les URLs contenant 'product'
                priority = 0 if "product" in link.lower() else 1
                self.queue.put((priority, link))

    def _calculate_metrics(self):
        """Calcule les métriques finales du crawling."""
        self.metrics["total_time"] = time.time() - self.start_time
        self.metrics["pages_per_second"] = self.metrics["pages_crawled"] / self.metrics["total_time"]
        return {
            "Pages crawlées": self.metrics["pages_crawled"],
            "Temps total (s)": round(self.metrics["total_time"], 2),
            "Pages par seconde": round(self.metrics["pages_per_second"], 2),
            "Erreurs rencontrées": self.metrics["errors"]
        }

    def run(self):
        """
        Lance le processus de crawling.
        """
        self.start_time = time.time()
        self.queue.put((0, self.start_url))
        
        while not self.queue.empty() and len(self.visited) < self.max_pages:
            priority, current_url = self.queue.get()
            
            if current_url in self.visited:
                continue
                
            print(f"Visite #{len(self.visited)+1}: {current_url}")
            
            # Vérification des robots.txt
            if not self._can_fetch(current_url):
                print(f"Crawling non autorisé pour: {current_url}")
                continue
            
            html = self._get_html(current_url)
            if not html:
                continue
                
            title, first_paragraph, links = self._extract_content(html, current_url)
            
            self.visited.add(current_url)
            self.metrics["pages_crawled"] += 1
            
            # Stockage des résultats
            self.results.append({
                "title": title,
                "url": current_url,
                "first_paragraph": first_paragraph,
                "links": links,
                "crawl_time": datetime.now().isoformat()
            })
            
            self._add_to_queue(links)
            time.sleep(self.delay)
        
        # Sauvegarde des résultats
        with open("results.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Affichage des métriques
        metrics = self._calculate_metrics()
        print("\nRésultats du crawling:")
        for key, value in metrics.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    crawler = WebCrawler("https://web-scraping.dev/products", max_pages=50)
    crawler.run()