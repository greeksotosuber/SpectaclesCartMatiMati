# data_manager.py
import pandas as pd
from product import Product

def read_excel(file_path):
    df = pd.read_excel(file_path)
    products = []
    for _, row in df.iterrows():
        tags = [tag.strip() for tag in row['Tags'].split(',')]
        products.append(Product(row['Name'], tags, row['Price'], row['Image']))  # 'Image' column has the path
    return products
