from database_manager import DatabaseManager
from models import User

class AuthSystem:
    def __init__(self):
        self.db = DatabaseManager("database/users.json")

    def login(self):
        phone = input("Telefon: ")
        password = input("Parol: ")
        data = self.db.load()

        for u in data["users"]:
            if u["phone"] == phone and u["password"] == password:
                return User(**u)

        print("Xato login yoki parol")
        return None

    def register(self):
        data = self.db.load()
        phone = input("Telefon: ")

        for u in data["users"]:
            if u["phone"] == phone:
                print("Bu raqam mavjud")
                return None

        new_user = {
            "id": len(data["users"]) + 1,
            "name": input("Ism: "),
            "phone": phone,
            "password": input("Parol: "),
            "role": "user",
            "membership": "bronze",
            "address": input("Manzil: "),
            "purchase_history": []
        }

        data["users"].append(new_user)
        self.db.save(data)
        print("Ro‘yxatdan o‘tdingiz")
