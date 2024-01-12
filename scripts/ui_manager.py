# ui_manager.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from data_manager import read_excel
from product import Product

class OpticsShopUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optics Shop")
        self.setGeometry(100, 100, 800, 600)  # Adjust size as needed

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.products_grid = QGridLayout()
        self.layout.addLayout(self.products_grid)

        self.cart = []
        self.total_price = 0
        self.discount = 0


        self.setStyleSheet("""
            QMainWindow { background-color: gray; }
            QLabel { font-family: Arial; font-size: 14px; }
            QPushButton { background-color: red; color: white; border-radius: 5px; }
            QPushButton:hover { background-color: darkred; }
            QLineEdit { border: 1px solid gray; }
        """)
        # Load products and display them
        self.products = read_excel("products.xlsx")
        self.display_products(self.products)

        # Cart and checkout UI elements
        self.cart_layout = QVBoxLayout()
        self.cart_label = QLabel("Cart:")
        self.cart_layout.addWidget(self.cart_label)
        self.layout.addLayout(self.cart_layout)

        self.checkout_layout = QHBoxLayout()
        self.total_label = QLabel("Total: €0")
        self.checkout_layout.addWidget(self.total_label)

        self.discount_input = QLineEdit()
        self.discount_input.setPlaceholderText("Discount %")
        self.checkout_layout.addWidget(self.discount_input)

        self.apply_discount_button = QPushButton("Apply Discount")
        self.apply_discount_button.clicked.connect(self.apply_discount)
        self.checkout_layout.addWidget(self.apply_discount_button)

        self.layout.addLayout(self.checkout_layout)

        self.clear_cart_button = QPushButton("Clear Cart")
        self.clear_cart_button.clicked.connect(self.clear_cart)
        self.checkout_layout.addWidget(self.clear_cart_button)

    def display_products(self, products):
        row = 0
        col = 0
        for product in products:
            # Vertical layout for each product
            product_layout = QVBoxLayout()

            # Create and set up the image label
            image_label = QLabel(self)
            pixmap = QPixmap(product.image_path)
            image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))  # Scale the image to fit
            product_layout.addWidget(image_label)

            # Create and add a label for the product name
            name_label = QLabel(product.name)
            product_layout.addWidget(name_label)

            # Create and add a label for the product price
            price_label = QLabel(f"€{product.price}")
            product_layout.addWidget(price_label)

            # Add to Cart button
            add_to_cart_button = QPushButton("Add to Cart", self)
            add_to_cart_button.clicked.connect(lambda _, p=product: self.add_to_cart(p))
            product_layout.addWidget(add_to_cart_button)

            # Create a container widget for the product layout
            container = QWidget()
            container.setLayout(product_layout)

            # Add the container to the grid
            self.products_grid.addWidget(container, row, col)

            # Update the column, and if necessary, move to the next row
            col += 1
            if col >= 3:  # Adjust the number of columns as needed
                row += 1
                col = 0



    def add_to_cart(self, product):
        self.cart.append(product)
        self.update_cart_display()

    def clear_cart(self):
            self.cart = []
            self.update_cart_display()

    def update_cart_display(self):
        # Clear the current cart display
        for i in reversed(range(self.cart_layout.count())): 
            widget = self.cart_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Update cart display with new contents
        self.total_price = 0
        for product in self.cart:
            product_label = QLabel(f"{product.name} - €{product.price}")
            self.cart_layout.addWidget(product_label)
            self.total_price += product.price

        # Update total price display
        self.total_label.setText(f"Total: €{self.total_price:.2f}")


    def apply_discount(self):
        try:
            discount_percentage = float(self.discount_input.text())
            discount_amount = self.total_price * (discount_percentage / 100)
            discounted_total = self.total_price - discount_amount
            self.total_label.setText(f"Total after discount: €{discounted_total:.2f}")
        except ValueError:
            # Handle the case where the discount input is not a valid number
            self.total_label.setText("Invalid discount. Please enter a valid number.")


# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = OpticsShopUI()
    main_window.show()
    sys.exit(app.exec_())
