class Product:
    def __init__(self):
        self.price = 0
        self.quantity = 0
        self.weight = 0

    def calc_shipping_cost(self):
        pass

    def calc_sales_tax(self):
        pass

    def calc_total(self):
        pass

    def display(self):
        pass


class Food(Product):
    def __init__(self):
        Product.__init__(self)
        self.age = 0
        self.size = 0
        self.type = 0
        self.expiration_date = 0


class Cheese(Food):
    def __init__(self):
        Food.__init__(self)


class Crackers(Food):
    def __init__(self):
        Food.__init__(self)
        self.flavor = 0
        self.shape = 0


class Tomagatchi(Product):
    def __init__(self):
        Product.__init__(self)
        self.color = 0