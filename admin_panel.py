from database_manager import DatabaseManager
from constants import CATEGORIES

class AdminPanel:
    def __init__(self):
        self.products_db = DatabaseManager("database/products.json")
        self.orders_db = DatabaseManager("database/orders.json")

    def menu(self):
        while True:
            print("\n--- ADMIN PANEL ---")
            print("1. Mahsulot qo‘shish")
            print("2. Mahsulotlarni ko‘rish")
            print("3. Mahsulotni o‘chirish")
            print("4. Mahsulotni yangilash")
            print("5. Sotuvlar tarixi")
            print("6. Chiqish")

            c = input(">>> ")

            if c == "1":
                self.add_product()
            elif c == "2":
                self.view_products()
            elif c == "3":
                self.delete_product()
            elif c == "4":
                self.update_product()
            elif c == "5":
                self.view_sales()
            elif c == "6":
                break


    def add_product(self):
        data = self.products_db.load()

        print("\nKategoriya tanlang:")
        for i, cat in enumerate(CATEGORIES, 1):
            print(f"{i}. {cat}")

        cat_index = int(input(">>> ")) - 1

        product = {
            "id": len(data["products"]) + 1,
            "name": input("Nomi: "),
            "category": CATEGORIES[cat_index],
            "price": float(input("Narx (USD): ")),
            "quantity": int(input("Soni: ")),
            "status": "active"
        }

        data["products"].append(product)
        self.products_db.save(data)
        print("✅ Mahsulot qo‘shildi")

    def view_products(self):
        data = self.products_db.load()
        print("\n--- MAHSULOTLAR ---")
        for p in data["products"]:
            print(
                f"ID:{p['id']} | {p['name']} | {p['category']} | "
                f"{p['price']} USD | Soni:{p['quantity']}"
            )

    def delete_product(self):
        data = self.products_db.load()
        pid = int(input("O‘chiriladigan mahsulot ID: "))

        data["products"] = [p for p in data["products"] if p["id"] != pid]
        self.products_db.save(data)
        print("🗑 Mahsulot o‘chirildi")

    def update_product(self):
        data = self.products_db.load()
        pid = int(input("Yangilanadigan mahsulot ID: "))

        for p in data["products"]:
            if p["id"] == pid:
                print("\nBo‘sh qoldirsangiz eski qiymat saqlanadi")

                new_name = input(f"Nomi ({p['name']}): ")
                new_price = input(f"Narx ({p['price']} USD): ")
                new_qty = input(f"Soni ({p['quantity']}): ")

                print("\nKategoriya tanlang (Enter bosilsa o‘zgarmaydi):")
                for i, cat in enumerate(CATEGORIES, 1):
                    print(f"{i}. {cat}")
                cat_input = input(">>> ")

                if new_name:
                    p["name"] = new_name
                if new_price:
                    p["price"] = float(new_price)
                if new_qty:
                    p["quantity"] = int(new_qty)
                if cat_input:
                    p["category"] = CATEGORIES[int(cat_input) - 1]

                self.products_db.save(data)
                print("✏️ Mahsulot yangilandi")
                return

        print("❌ Mahsulot topilmadi")


    def view_sales(self):
        orders = self.orders_db.load()["orders"]
        if not orders:
            print("Sotuv yo‘q")
            return

        print("\n--- SOTUVLAR TARIXI ---")
        for o in orders:
            print(o)
