import requests
from bs4 import BeautifulSoup
from categories import Categories
from livres import Livres
import csv
import os


class Scraping:
    def __init__(self, site_url, ):

        self.site_url = site_url
        self.categories = []
        self.book_links = []
        self.books = []
        self.en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax",
                        "price_excluding_tax", "number_available", "product_description", "category",
                        "review_rating", "image_url"]

    def scrape_categories(self):
        os.makedirs('csv', exist_ok=True)
        response = requests.get(self.site_url)
        if response.ok:
            print("connexion au site ok")
            soup = BeautifulSoup(response.text, "html.parser")
            category_elements = soup.find("ul", class_="nav nav-list").find_all("li")[1:]

            for element in category_elements:
                name = element.find("a").text.strip()
                url = "https://books.toscrape.com/" + element.find("a")["href"]
                category = Categories(name=name, url=url)
                self.categories.append(category)

                csv_filename = f"csv/{name.replace(' ', '_').lower()}.csv"
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file, delimiter=',')
                    writer.writerow(self.en_tete)
        return self.categories

    def scrape_book_links(self):

        for category in self.categories:
            print(f"Enregistrement des liens des livres pour la catégorie: {category.name}")
            page_num = 1

            while True:
                url = category.url.replace("index.html", f"page-{page_num}.html") if page_num > 1 else category.url
                response = requests.get(url)
                if response.ok:
                    soup = BeautifulSoup(response.text, "html.parser")
                    products = soup.find_all("h3")
                    if not products:
                        break
                    for product in products:
                        product_url = "https://books.toscrape.com/catalogue" + product.find("a")["href"].replace(
                            "../../..", "")
                        self.book_links.append([product_url, category.name])
                else:
                    break
                page_num += 1
        return self.book_links

    def scrape_book_details(self):
        os.makedirs('images', exist_ok=True)

        index = 1
        for book_url, category_name in self.book_links:

            print(f"Scraping du livre: {index}/{len(self.book_links)} - URL: {book_url}")
            index += 1
            response = requests.get(book_url)

            if response.ok:
                soup = BeautifulSoup(response.text, "html.parser")
                title = soup.find("title").text.strip()
                upc = soup.find("th", string="UPC").find_next_sibling("td").text
                price_inc = soup.find("th", string="Price (incl. tax)").find_next_sibling("td").text[1:]
                price_exc = soup.find("th", string="Price (excl. tax)").find_next_sibling("td").text[1:]
                availability_text = soup.find("th", string="Availability").find_next_sibling("td").text
                number_available = availability_text.split()[2][1:]

                try:
                    description = soup.find(id="product_description").find_next_sibling("p").text.strip()
                except AttributeError:
                    description = "Pas de description disponible."

                rating_class = soup.find(class_="star-rating")['class'][1]

                image_before = soup.find("img")
                image_url = "https://books.toscrape.com/" + image_before["src"].replace("../..", "")

                book = Livres(
                    product_page_url=book_url,
                    universal_product_code=upc,
                    title=title,
                    price_including_tax=price_inc,
                    price_excluding_tax=price_exc,
                    number_available=number_available,
                    product_description=description,
                    category=category_name,
                    review_rating=rating_class,
                    image_url=image_url
                )

                self.books.append(book)

            image_response = requests.get(image_url)
            image_filename = f"images/{upc}.jpg"
            with open(image_filename, 'wb') as file:
                file.write(image_response.content)

            csv_filename = f"csv/{category_name.replace(' ', '_').lower()}.csv"
            informations = [
                book.product_page_url, book.universal_product_code, book.title, book.price_including_tax,
                book.price_excluding_tax, book.number_available, book.product_description,
                book.category, book.rating_value(), book.image_url
            ]
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(informations)

        return self.books
