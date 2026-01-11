from auth import AuthSystem
from admin_panel import AdminPanel
from user_panel import UserPanel

auth = AuthSystem()

while True:
    print("\n1. Login")
    print("2. Register")
    print("3. Exit")

    c = input(">>> ")

    if c == "1":
        user = auth.login()
        if user:
            if user.role == "admin":
                AdminPanel().menu()
            else:
                UserPanel(user).menu()

    elif c == "2":
        auth.register()

    elif c == "3":
        break
