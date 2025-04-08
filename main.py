from scraping import Scraping


def main():
    site_url = "https://books.toscrape.com/index.html"
    print("Démarrage du Script")
    scraper = Scraping(site_url=site_url)
    print("Recuperation des catégories")
    categories = scraper.scrape_categories()
    print(f"Catégories trouvées ({len(categories)}): ")
    print("\nScraping des liens des livres dans chaque catégorie...")
    book_links = scraper.scrape_book_links()
    print(f"Liens des livres trouvés ({len(book_links)}): ")
    print("\nRécuperation des détails des livres + sauvegarde image + sauvegarde CSV en cours...")
    scraper.scrape_book_details()
    print("\nScripts terminé. Vérifiez les fichiers CSV et le répertoire images.")


if __name__ == "__main__":
    main()
