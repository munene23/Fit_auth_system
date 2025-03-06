import hashlib
from typing import Optional, Dict
from models import User, Role
from repository import UserRepository

class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.sessions: Dict[str, str] = {}  # session_id: email

    def register(self, first_name: str, last_name: str, phone_number: str,
                 date_of_birth: str, email: str, password: str) -> bool:
        return self.repository.add_user(first_name, last_name, phone_number, date_of_birth, email, password)

    def login(self, email: str, password: str) -> Optional[str]:
        user = self.repository.get_user(email)
        if not user or user.password_hash != hashlib.sha256(password.encode()).hexdigest():
            return None
        session_id = hashlib.sha256(f"{email}{password}".encode()).hexdigest()
        self.sessions[session_id] = email
        return session_id

    def logout(self, session_id: str) -> bool:
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def get_user_from_session(self, session_id: str) -> Optional[User]:
        email = self.sessions.get(session_id)
        return self.repository.get_user(email) if email else None

    def require_role(self, session_id: str, required_role: Role) -> bool:
        user = self.get_user_from_session(session_id)
        return user is not None and user.role == required_role

    def update_profile(self, session_id: str, first_name: str = None, last_name: str = None,
                       phone_number: str = None, date_of_birth: str = None,
                       email: str = None, password: str = None) -> bool:
        user = self.get_user_from_session(session_id)
        if not user:
            return False
        return self.repository.update_user(user.email, first_name, last_name, phone_number,
                                          date_of_birth, email, password)

    def get_user_data(self, session_id: str) -> Optional[dict]:
        user = self.get_user_from_session(session_id)
        return user.to_dict() if user else None