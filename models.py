class User:
    def __init__(self, id, name, phone, password, role, membership, address, purchase_history):
        self.id = id
        self.name = name
        self.phone = phone
        self.password = password
        self.role = role
        self.membership = membership
        self.address = address
        self.purchase_history = purchase_history


class Product:
    def __init__(self, id, name, category, price, quantity, status="active"):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.status = status


class Order:
    def __init__(self, order_id, user_id, products, delivery_type, date):
        self.order_id = order_id
        self.user_id = user_id
        self.products = products
        self.delivery_type = delivery_type
        self.date = date
