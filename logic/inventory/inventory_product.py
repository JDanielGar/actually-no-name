class Product(object):
    def __init__(self, product_id, product_name, sale_value, purchase_value, stock):
        self.product_id = product_id
        self.product_name = product_name
        self.sale_value = sale_value
        self.purchase_value = purchase_value
        self.stock = stock
    def change_id(self, product_id):
        self.product_id = product_id
    def change_name(self, product_name):
        self.product_name = product_name
    def change_sale_value(self, sale_value):
        self.sale_value = sale_value
    def change_purchase_value(self, purchase_value):
        self.purchase_value = purchase_value
    def change_stock(self, stock):
        self.stock = stock