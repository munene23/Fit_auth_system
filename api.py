from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from typing import Optional

from auth_service import AuthService
from repository import UserRepository
from models import Role

class AuthAPIHandler(BaseHTTPRequestHandler):
    def __init__(self, auth_service: AuthService, *args, **kwargs):
        self.auth_service = auth_service
        super().__init__(*args, **kwargs)

    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _require_session(self) -> Optional[str]:
        session_id = self.headers.get("X-Session-ID")
        if not session_id or not self.auth_service.get_user_from_session(session_id):
            self._set_headers(401)
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
            return None
        return session_id

    # Register: POST /register
    def do_POST(self):
        if self.path == "/register":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode())
                first_name = data["first_name"]
                last_name = data["last_name"]
                phone_number = data["phone_number"]
                date_of_birth = data["date_of_birth"]
                email = data["email"]
                password = data["password"]
                if self.auth_service.register(first_name, last_name, phone_number, date_of_birth, email, password):
                    self._set_headers(201)
                    self.wfile.write(json.dumps({"message": "User registered", "email": email}).encode())
                else:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": "Email already exists"}).encode())
            except (KeyError, json.JSONDecodeError):
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid request data"}).encode())

        # Login: POST /login
        elif self.path == "/login":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode())
                email = data["email"]
                password = data["password"]
                session_id = self.auth_service.login(email, password)
                if session_id:
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"session_id": session_id}).encode())
                else:
                    self._set_headers(401)
                    self.wfile.write(json.dumps({"error": "Invalid credentials"}).encode())
            except (KeyError, json.JSONDecodeError):
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid request data"}).encode())

        # Update Profile: POST /profile
        elif self.path == "/profile":
            session_id = self._require_session()
            if not session_id:
                return
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode())
                first_name = data.get("first_name")
                last_name = data.get("last_name")
                phone_number = data.get("phone_number")
                date_of_birth = data.get("date_of_birth")
                email = data.get("email")
                password = data.get("password")
                if self.auth_service.update_profile(session_id, first_name, last_name, phone_number,
                                                   date_of_birth, email, password):
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"message": "Profile updated"}).encode())
                else:
                    self._set_headers(500)
                    self.wfile.write(json.dumps({"error": "Update failed"}).encode())
            except json.JSONDecodeError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())

        # Admin Create User: POST /users
        elif self.path == "/users":
            session_id = self._require_session()
            if not session_id or not self.auth_service.require_role(session_id, Role.ADMIN):
                self._set_headers(403)
                self.wfile.write(json.dumps({"error": "Admin access required"}).encode())
                return
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode())
                first_name = data["first_name"]
                last_name = data["last_name"]
                phone_number = data["phone_number"]
                date_of_birth = data["date_of_birth"]
                email = data["email"]
                password = data["password"]
                role = Role[data.get("role", "USER").upper()]
                if self.auth_service.repository.add_user(first_name, last_name, phone_number,
                                                        date_of_birth, email, password, role):
                    self._set_headers(201)
                    self.wfile.write(json.dumps({"message": "User created", "email": email}).encode())
                else:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": "Email already exists"}).encode())
            except (KeyError, json.JSONDecodeError, ValueError):
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid request data"}).encode())

    # Get Profile: GET /profile
    def do_GET(self):
        if self.path == "/profile":
            session_id = self._require_session()
            if not session_id:
                return
            user_data = self.auth_service.get_user_data(session_id)
            self._set_headers(200)
            self.wfile.write(json.dumps(user_data).encode())

        # Admin List Users: GET /users
        elif self.path == "/users":
            session_id = self._require_session()
            if not session_id or not self.auth_service.require_role(session_id, Role.ADMIN):
                self._set_headers(403)
                self.wfile.write(json.dumps({"error": "Admin access required"}).encode())
                return
            users = self.auth_service.repository.list_users()
            self._set_headers(200)
            self.wfile.write(json.dumps(users).encode())

        # Admin Read User: GET /users/{email}
        elif self.path.startswith("/users/"):
            session_id = self._require_session()
            if not session_id or not self.auth_service.require_role(session_id, Role.ADMIN):
                self._set_headers(403)
                self.wfile.write(json.dumps({"error": "Admin access required"}).encode())
                return
            email = self.path.split("/")[-1]
            user = self.auth_service.repository.get_user(email)
            if user:
                self._set_headers(200)
                self.wfile.write(json.dumps(user.to_dict()).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "User not found"}).encode())

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    # Admin Update User: PUT /users/{email}
    def do_PUT(self):
        if self.path.startswith("/users/"):
            session_id = self._require_session()
            if not session_id or not self.auth_service.require_role(session_id, Role.ADMIN):
                self._set_headers(403)
                self.wfile.write(json.dumps({"error": "Admin access required"}).encode())
                return
            email = self.path.split("/")[-1]
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode())
                first_name = data.get("first_name")
                last_name = data.get("last_name")
                phone_number = data.get("phone_number")
                date_of_birth = data.get("date_of_birth")
                new_email = data.get("email")
                password = data.get("password")
                role = Role[data["role"].upper()] if "role" in data else None
                if self.auth_service.repository.update_user(email, first_name, last_name, phone_number,
                                                          date_of_birth, new_email, password, role):
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"message": "User updated"}).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "User not found"}).encode())
            except (json.JSONDecodeError, ValueError):
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid request data"}).encode())

    # Logout: DELETE /logout
    # Admin Delete User: DELETE /users/{email}
    def do_DELETE(self):
        if self.path == "/logout":
            session_id = self._require_session()
            if not session_id:
                return
            if self.auth_service.logout(session_id):
                self._set_headers(204)
                self.wfile.write(b"")
            else:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": "Logout failed"}).encode())

        elif self.path.startswith("/users/"):
            session_id = self._require_session()
            if not session_id or not self.auth_service.require_role(session_id, Role.ADMIN):
                self._set_headers(403)
                self.wfile.write(json.dumps({"error": "Admin access required"}).encode())
                return
            email = self.path.split("/")[-1]
            if self.auth_service.repository.delete_user(email):
                self._set_headers(204)
                self.wfile.write(b"")
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "User not found"}).encode())

# Factory for dependency injection
def create_handler(auth_service):
    def handler(*args, **kwargs):
        return AuthAPIHandler(auth_service, *args, **kwargs)
    return handler

def run_server(port=8000):
    repo = UserRepository()
    auth_service = AuthService(repo)
    server_address = ("", port)
    httpd = HTTPServer(server_address, create_handler(auth_service))
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()