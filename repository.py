from typing import Dict, Optional
from models import User, Role

class UserRepository:
    def __init__(self):
        self.users: Dict[str, User] = {}  # Key is email now
        # Seed an admin user
        self.add_user("Admin", "User", "1234567890", "1980-01-01", "admin@example.com", "admin123", Role.ADMIN)

    def add_user(self, first_name: str, last_name: str, phone_number: str,
                 date_of_birth: str, email: str, password: str, role: Role = Role.USER) -> bool:
        if email in self.users:
            return False
        self.users[email] = User(first_name, last_name, phone_number, date_of_birth, email, password, role)
        return True

    def get_user(self, email: str) -> Optional[User]:
        return self.users.get(email)

    def update_user(self, email: str, first_name: str = None, last_name: str = None,
                    phone_number: str = None, date_of_birth: str = None,
                    new_email: str = None, password: str = None, role: Role = None) -> bool:
        user = self.users.get(email)
        if not user:
            return False
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if phone_number:
            user.phone_number = phone_number
        if date_of_birth:
            user.date_of_birth = date_of_birth
        if new_email and new_email != email:
            if new_email in self.users:
                return False
            self.users[new_email] = user
            del self.users[email]
            user.email = new_email
        if password:
            user.password_hash = hashlib.sha256(password.encode()).hexdigest()
        if role:
            user.role = role
        return True

    def delete_user(self, email: str) -> bool:
        if email in self.users:
            del self.users[email]
            return True
        return False

    def list_users(self) -> list:
        return [user.to_dict() for user in self.users.values()]