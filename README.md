User Data Format
json

{
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string",
    "date_of_birth": "YYYY-MM-DD",
    "email": "string",
    "role": "USER|ADMIN"
}

Testing with Postman
Start the Server:
Run api.py

Test Registration:
POST http://localhost:8000/register

Body:
json

{
    "first_name": "Brian",
    "last_name": "Smith",
    "phone_number": "1234567890",
    "date_of_birth": "1995-05-15",
    "email": "brian@example.com",
    "password": "brian123"
}

Test Login:
POST http://localhost:8000/login

Body: {"email": "brian@example.com", "password": "brian123"}



Test Profile:
GET http://localhost:8000/profile

Headers: X-Session-ID: <session_id>

Test Admin Features:
Log in as admin (admin@example.com/admin123) to get an admin session ID.

Use it to test /users endpoints.

