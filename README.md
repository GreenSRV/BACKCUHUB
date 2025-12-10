# CU Hub – Backend API (Flask + MongoDB)

Backend service for **CU Hub**, a platform that helps Chulalongkorn University students discover, join, create, and rate student clubs.  
Built with **Flask**, **MongoDB Atlas**, and **Marshmallow** for schema validation.

---

## 🚀 Features

### 👤 Student Management
- Register new students  
- Login with student ID + password  
- Add/remove joined clubs  
- Fetch student’s club list  
- Update student details (except `student_id`)  
- Delete student account  

### 🏛️ Club Management
- Add new clubs  
- Search clubs  
- Update club information (except club name)  
- Delete clubs  
- Rate clubs (rating 1–5)  
- Fetch average ratings  

### ⭐ Club Rating System
- Each club stores an array of ratings  
- Average rating is auto-calculated on fetch  

### 🔍 Search Functionality
- Search students by ID  
- Search clubs by name (case-insensitive)

---

## 🛠️ Tech Stack
- **Backend:** Flask (Python)  
- **Database:** MongoDB Atlas (NoSQL)  
- **Validation:** Marshmallow  
- **JSON Handling:** BSON / `json_util`  
- **Testing:** Postman  

---

## 📦 Project Structure


/models
user_model.py # StudentSchema & ClubSchema

/routes
user_routes.py # All student + club CRUD routes

/utils
response.py # success_response, error_response, validators

app.py # Flask main app entry


---

## 📘 API Endpoints

### General
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ping` | Health check |

### Student Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/students` | Add new student |
| GET | `/students` | Get all students (search optional) |
| POST | `/students/login` | Login student |
| PUT | `/students/<id>` | Update student (cannot change ID) |
| PUT | `/students/<id>/addclub` | Add club to student |
| PUT | `/students/<id>/removeclub` | Remove club from student |
| GET | `/students/<id>/clubs` | Get clubs joined by student |
| DELETE | `/students/<id>` | Delete student |

### Club Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/clubs` | Add new club |
| GET | `/clubs` | Get all clubs (search optional) |
| PUT | `/clubs/<name>` | Update club (name cannot change) |
| DELETE | `/clubs/<name>` | Delete club |
| PUT | `/clubs/<name>/rate` | Add rating to a club |
| POST | `/clubs/rating/<id>` | Rate club by student (legacy route) |

---

## 🧪 Example Requests

### **Add Student** — `POST /students`
{
  "student_id": "65012345",
  "password": "1234",
  "club": []
}

### Add Club — POST /clubs
{
  "name": "CU Football Club",
  "category": "Sports",
  "date": "2025-01-15",
  "faculty": "ENG",
  "image": "url_here",
  "members": "120"
}

### Rate a Club — PUT /clubs/<name>/rate
{
  "rating": 5
}

## 🧰 Validation Using Marshmallow
### StudentSchema

student_id (required)

password (required)

club — list of strings

### ClubSchema

name, category, date, faculty, image, members (required)

ratings — list of integers

average_rating — computed

## 🔒 Error Handling

### Error Response

{
  "status": "error",
  "message": "Student ID already exists"
}


### Success Response

{
  "status": "success",
  "message": "Student added successfully"
}

## 🖥️ Running the Backend
### 1. Install dependencies
pip install -r requirements.txt

### 2. Set MongoDB connection

Inside app.py:

app.mongo = PyMongo(app, uri="your-mongodb-atlas-uri")

### 3. Run server
flask run

## 🎓 About CU Hub

CU Hub is designed to simplify:
- discovering clubs
- joining clubs
- managing student membership
- rating and reviewing clubs
- creating new clubs

This backend powers the frontend built with React Native + NativeWind.
