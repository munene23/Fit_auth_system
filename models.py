import hashlib
from enum import Enum
from datetime import datetime

class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class User:
    def __init__(self, first_name: str, last_name: str, phone_number: str,
                 date_of_birth: str, email: str, password: str, role: Role = Role.USER):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth  # Expected format: "YYYY-MM-DD"
        self.email = email
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.role = role

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "date_of_birth": self.date_of_birth,
            "email": self.email,
            "role": self.role.value
        }