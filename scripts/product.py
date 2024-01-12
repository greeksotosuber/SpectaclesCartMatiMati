# product.py

class Product:
    def __init__(self, name, tags, price, image_path):
        self.name = name
        self.tags = tags
        self.price = price
        self.image_path = image_path  # Path to the local image file
