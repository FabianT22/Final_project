class Product:

    def __init__(self, product_price, product_href, start_date, end_date, id_product, product_name):
        self.product_price = product_price
        self.product_href = product_href
        self.start_date = start_date
        self.end_date = end_date
        self.id_product = id_product
        self.product_name = product_name
    # object string representation
    def __repr__(self):
        return(' Product name: ' + str(self.product_name) + '\n' +
               ' Product price: ' + str(self.product_price) + '\n' +
               ' Product price start date: ' + str(self.start_date) + '\n' +
               ' Product price end date: ' + str(self.end_date) + '\n' +
               ' Product id: ' + str(self.id_product) + '\n' +
               ' Product link: ' + str(self.product_href)
               )
    # class equality
    def __eq__(self, other):
        if isinstance(other, Product):
            if self.product_name == other.product_name and self.product_price == other.product_price:
                return True
            else:
                return False
    # class greater than
    def __gt__(self, other):
        if isinstance(other, Product):
            if self.product_price > other.product_price:
                return True
            else:
                return False
    # class less than
    def __lt__(self, other):
        if isinstance(other, Product):
            if self.price < other.product_price:
                return True
            else:
                return False

