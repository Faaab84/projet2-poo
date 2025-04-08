class Livres:
    def __init__(self, product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                 number_available, product_description, category, review_rating, image_url):
        self.product_page_url = product_page_url
        self.universal_product_code = universal_product_code
        self.title = title
        self.price_including_tax = price_including_tax
        self.price_excluding_tax = price_excluding_tax
        self.number_available = number_available
        self.product_description = product_description
        self.review_rating = review_rating
        self.image_url = image_url
        self.category = category

    def __str__(self):
        return f"Titre: {self.title}\nCodeUPC: {self.universal_product_code}\nPrix (incl. tax): {self.price_including_tax}\n  \
        Prix (excl. tax): {self.price_excluding_tax}\nDisponibilitée: {self.number_available}\n" \
               f"Description: {self.product_description}\nNote: {self.rating_value()}\n" \
               f"Image URL: {self.image_url}\nCategorie: {self.category}"

    def rating_value(self):
        star = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        return star.get(self.review_rating, None)
