from database_manager import DatabaseManager
from constants import CATEGORIES, MEMBERSHIP_DISCOUNT
from datetime import datetime

class UserPanel:
    def __init__(self, user):
        self.user = user
        self.products_db = DatabaseManager("database/products.json")
        self.orders_db = DatabaseManager("database/orders.json")
        self.cart = [] 


    def menu(self):
        while True:
            print(f"\n--- USER PANEL ({self.user.membership.upper()}) ---")
            print("1. Mahsulotlarni ko‘rish")
            print("2. Kategoriya bo‘yicha ko‘rish")
            print("3. Qidirish")
            print("4. Savatchani ko‘rish")
            print("5. Mening buyurtmalarim")
            print("6. A’zolikni o‘zgartirish")
            print("7. Chiqish")

            c = input(">>> ")

            if c == "1":
                self.view_products()
            elif c == "2":
                self.view_by_category()
            elif c == "3":
                self.search()
            elif c == "4":
                self.view_cart()
            elif c == "5":
                self.view_my_orders()
            elif c == "6":
                self.change_membership()
            elif c == "7":
                break


    def view_products(self):
        products = self.products_db.load()["products"]
        print("\n--- MAHSULOTLAR ---")
        for p in products:
            print(f"{p['id']} | {p['name']} | {p['price']} USD")
        self.add_to_cart()

    def view_by_category(self):
        print("\n--- KATEGORIYALAR ---")
        for i, c in enumerate(CATEGORIES, 1):
            print(f"{i}. {c}")

        idx = int(input(">>> ")) - 1
        products = self.products_db.load()["products"]

        print("\n--- MAHSULOTLAR ---")
        for p in products:
            if p["category"] == CATEGORIES[idx]:
                print(f"{p['id']} | {p['name']} | {p['price']} USD")

        self.add_to_cart()

    def search(self):
        key = input("Qidiruv so‘zi: ").lower()
        products = self.products_db.load()["products"]

        print("\n--- QIDIRUV NATIJASI ---")
        for p in products:
            if key in p["name"].lower():
                print(f"{p['id']} | {p['name']} | {p['price']} USD")

        self.add_to_cart()

    def add_to_cart(self):
        choice = input("Savatchaga qo‘shasizmi? (y/n): ")
        if choice.lower() == "y":
            pid = int(input("Mahsulot ID: "))
            qty = int(input("Soni: "))
            self.cart.append({"product_id": pid, "quantity": qty})
            print("🛒 Savatchaga qo‘shildi")


    def view_cart(self):
        if not self.cart:
            print("🛒 Savatcha bo‘sh")
            return

        print("\n--- SAVATCHA ---")
        products = self.products_db.load()["products"]

        total = 0
        for i, item in enumerate(self.cart, 1):
            for p in products:
                if p["id"] == item["product_id"]:
                    item_total = p["price"] * item["quantity"]
                    total += item_total
                    print(
                        f"{i}. {p['name']} | "
                        f"{item['quantity']} x {p['price']} USD = {item_total} USD"
                    )

        discount = MEMBERSHIP_DISCOUNT[self.user.membership]
        discounted_total = total - (total * discount / 100)

        print(f"\nJami: {total} USD")
        print(f"A’zolik chegirmasi: {discount}%")
        print(f"To‘lanadi: {discounted_total} USD")

        while True:
            print("\n1. Buyurtma berish")
            print("2. Savatchani bo‘shatish")
            print("3. Orqaga qaytish")

            c = input(">>> ")

            if c == "1":
                self.checkout()
                return
            elif c == "2":
                self.cart = []
                print("🗑 Savatcha tozalandi")
                return
            elif c == "3":
                return
            else:
                print("Noto‘g‘ri tanlov")


    def checkout(self):
        orders = self.orders_db.load()

        orders["orders"].append({
            "order_id": len(orders["orders"]) + 1,
            "user_id": self.user.id,
            "products": self.cart,
            "delivery_type": input("delivery / pickup: "),
            "date": str(datetime.now())
        })

        self.orders_db.save(orders)
        self.cart = []
        print("✅ Buyurtma qabul qilindi")

    def view_my_orders(self):
        orders = self.orders_db.load()["orders"]
        products = self.products_db.load()["products"]

        user_orders = [o for o in orders if o["user_id"] == self.user.id]

        if not user_orders:
            print("📭 Sizda hali buyurtmalar yo‘q")
            return

        print("\n--- MENING BUYURTMALARIM ---")

        for o in user_orders:
            print(f"\nBuyurtma ID: {o['order_id']}")
            print(f"Sana: {o['date']}")
            print(f"Yetkazish turi: {o['delivery_type']}")
            print("Mahsulotlar:")

            for item in o["products"]:
                for p in products:
                    if p["id"] == item["product_id"]:
                        print(
                            f"- {p['name']} | "
                            f"{item['quantity']} x {p['price']} USD"
                        )

            print("-" * 30)


    def change_membership(self):
        print("\n1. bronze\n2. silver\n3. gold\n4. business")
        c = int(input(">>> "))
        self.user.membership = ["bronze", "silver", "gold", "business"][c - 1]
        print("🎖 A’zolik yangilandi")
