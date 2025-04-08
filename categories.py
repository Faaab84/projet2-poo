class Categories:

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return f"Catégorie: {self.name}\nURL: {self.url}"
