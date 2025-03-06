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

Admin CRUD Operations



you’ll need to log in as the admin (admin@example.com/admin123) to get a session ID, then use it with the /users endpoints in Postman.

. CRUD Operations
Use the X-Session-ID: <admin_session_id> header for all requests.
Create a User
POST http://localhost:8000/users

Body: 
json

{
    "first_name": "Brian",
    "last_name": "Smith",
    "phone_number": "1234567890",
    "date_of_birth": "1995-05-15",
    "email": "brian@gmail.com",
    "password": "brian123",
    "role": "USER"
}

Response: 201 - {"message": "User created", "email": "brian@gmail.com"}

Read All Users
GET http://localhost:8000/users

Response: 200 - Array of users (e.g., [{"first_name": "Admin", ...}, {"first_name": "Brian", ...}])

Read One User
GET http://localhost:8000/users/brian@gmail.com

Response: 200 - {"first_name": "Brian", "last_name": "Smith", ...}

Update a User
PUT http://localhost:8000/users/brian@gmail.com

Body: 
json

{"last_name": "brian", "phone_number": "0787654321"}

Response: 200 - {"message": "User updated"}

Delete a User
DELETE http://localhost:8000/users/brian@gmail.com



Use it to test /users endpoints.

