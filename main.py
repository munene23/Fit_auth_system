from auth_service import AuthService
from repository import UserRepository
from models import Role

def main():
    repo = UserRepository()
    auth = AuthService(repo)
    print("Welcome to the Auth System!")

    while True:
        print("\nOptions: login, logout, update_profile, admin_crud, exit")
        choice = input("Choose an action: ").strip().lower()

        if choice == "exit":
            break

        elif choice == "login":
            username = input("Username: ")
            password = input("Password: ")
            session_id = auth.login(username, password)
            if session_id:
                print(f"Logged in! Session ID: {session_id}")
            else:
                print("Login failed.")

        elif choice == "logout":
            session_id = input("Session ID: ")
            if auth.logout(session_id):
                print("Logged out successfully.")
            else:
                print("Logout failed.")

        elif choice == "update_profile":
            session_id = input("Session ID: ")
            email = input("New email (leave blank to skip): ") or None
            password = input("New password (leave blank to skip): ") or None
            if auth.update_profile(session_id, email, password):
                print("Profile updated.")
            else:
                print("Update failed. Check session ID.")

        elif choice == "admin_crud":
            session_id = input("Admin Session ID: ")
            if not auth.require_role(session_id, Role.ADMIN):
                print("Admin access required.")
                continue
            action = input("CRUD Action (create/read/update/delete/list): ").strip().lower()

            if action == "create":
                username = input("New username: ")
                password = input("New password: ")
                email = input("New email: ")
                role = Role[input("Role (USER/ADMIN): ").upper()]
                if repo.add_user(username, password, email, role):
                    print("User created.")
                else:
                    print("Creation failed.")

            elif action == "read":
                username = input("Username to read: ")
                user = repo.get_user(username)
                print(user.to_dict() if user else "User not found.")

            elif action == "update":
                username = input("Username to update: ")
                email = input("New email (leave blank to skip): ") or None
                password = input("New password (leave blank to skip): ") or None
                role_str = input("New role (USER/ADMIN, leave blank to skip): ").upper()
                role = Role[role_str] if role_str in Role.__members__ else None
                if repo.update_user(username, email, password, role):
                    print("User updated.")
                else:
                    print("Update failed.")

            elif action == "delete":
                username = input("Username to delete: ")
                if repo.delete_user(username):
                    print("User deleted.")
                else:
                    print("Deletion failed.")

            elif action == "list":
                users = repo.list_users()
                print(users if users else "No users found.")

if __name__ == "__main__":
    main()