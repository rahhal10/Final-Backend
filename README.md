# 📚 Course Enrollment Backend (Express + PostgreSQL)

This is the **backend** for a course enrollment web app. It provides APIs for user authentication, course management, enrollment, and admin operations.


## 🏗️ Tech Stack

- Node.js + Express
- PostgreSQL (via `pg`)
- `dotenv`, `cors`, `morgan`


## 🚀 Getting Started

```bash
# 1. Install dependencies
npm install

# 2. Create a PostgreSQL database (e.g., `coursesdb`)

# 3. Start PostgreSQL and create DB tables
# (You may need to run your own schema.sql)

# 4. Start the server
node Server.js
```


## 🗂️ Project Structure
```
Final-Backend/
├── Routes/
│   ├── admin.js      # Admin endpoints
│   └── user.js       # User endpoints
├── db.js             # pg client
├── Server.js         # app entry
└── package.json
```


## 📡 API Endpoints

The API will run on: http://localhost:5000

---

### 👤 User Routes

**Base URL**: `/api/users`

| Method | Endpoint                | Description                        |
|--------|-------------------------|------------------------------------|
| GET    | `/courses`              | Get all available courses          |
| POST   | `/user-courses`         | Get courses a user is enrolled in  |
| POST   | `/Login`                | User login                         |
| POST   | `/addCart`              | Add course to cart                 |
| POST   | `/showcart`             | Get all items in user's cart       |
| DELETE | `/delcart`              | Delete item from cart              |
| PUT    | `/updatecartquantity`   | Update cart item quantity          |
| POST   | `/addcoursestouser`     | Enroll user in a course            |
| GET    | `/assignments`          | Get all assignments                |
| POST   | `/signup`               | Register new user                  |

#### 🔸 POST `/api/users/signup`
Registers a new user (student or admin).
```json
{
	"username": "student1",
	"email": "student1@example.com",
	"password": "123456",
	"role": "user"
}
```

#### 🔸 POST `/api/users/Login`
User login.
```json
{
	"email": "student1@example.com",
	"password": "123456"
}
```

#### 🔸 POST `/api/users/addCart`
Add a course to the user's cart.
```json
{
	"username": "student1",
	"email": "student1@example.com",
	"title": "React Basics",
	"description": "Learn React fundamentals",
	"instructor": "Jane Doe",
	"price": 100,
	"category": "Web Development",
	"duration": "4 weeks",
	"lessons_count": 12,
	"rating": 4.5,
	"image_url": "http://...",
	"quantity": 1
}
```

#### 🔸 POST `/api/users/showcart`
Get all items in the user's cart.
```json
{
	"email": "student1@example.com"
}
```

#### 🔸 DELETE `/api/users/delcart`
Delete an item from the cart.
```json
{
	"id": 1
}
```

#### 🔸 PUT `/api/users/updatecartquantity`
Update the quantity of a cart item.
```json
{
	"id": 1,
	"quantity": 2
}
```

#### 🔸 POST `/api/users/addcoursestouser`
Enroll a user in a course.
```json
{
	"username": "student1",
	"email": "student1@example.com",
	"title": "React Basics",
	"description": "Learn React fundamentals",
	"instructor": "Jane Doe",
	"price": 100,
	"category": "Web Development",
	"duration": "4 weeks",
	"lessons_count": 12,
	"rating": 4.5,
	"image_url": "http://..."
}
```

#### 🔸 POST `/api/users/user-courses`
Get all courses a user is enrolled in.
```json
{
	"email": "student1@example.com",
	"username": "student1"
}
```

#### 🔸 GET `/api/users/assignments`
Returns all assignments (tasks).

---

### 🛠️ Admin Routes

**Base URL**: `/api/admin`

| Method | Endpoint              | Description                        |
|--------|-----------------------|------------------------------------|
| GET    | `/usercount`          | Get total number of users          |
| GET    | `/coursescount`       | Get total number of courses        |
| GET    | `/admincourses`       | Get all courses (summary)          |
| DELETE | `/deladmincourses`    | Delete a course by ID              |
| PUT    | `/editadmincourse`    | Update course instructor           |
| POST   | `/addadmincourse`     | Add a new course                   |
| GET    | `/adminusers`         | Get all users                      |
| POST   | `/addadminuser`       | Add a new user                     |
| DELETE | `/deluser`            | Delete a user by ID                |

#### 🔸 POST `/api/admin/addadmincourse`
Add a new course.
```json
{
	"title": "React Basics",
	"description": "Learn React fundamentals",
	"instructor": "Jane Doe",
	"rating": 4.5,
	"duration": "4 weeks",
	"lessonsCount": 12,
	"price": 100,
	"imageUrl": "http://...",
	"category": "Web Development"
}
```

#### 🔸 PUT `/api/admin/editadmincourse`
Update a course's instructor.
```json
{
	"id": 1,
	"instructor": "John Smith"
}
```

#### 🔸 DELETE `/api/admin/deladmincourses`
Delete a course by ID.
```json
{
	"id": 1
}
```

#### 🔸 POST `/api/admin/addadminuser`
Add a new user (admin or student).
```json
{
	"email": "admin@example.com",
	"username": "admin1",
	"password": "123456",
	"role": "admin"
}
```

#### 🔸 DELETE `/api/admin/deluser`
Delete a user by ID.
```json
{
	"id": 1
}
```

---

## 📝 Notes
- All endpoints return errors in the format: `{ "error": "message" }` on failure.
- All endpoints require the appropriate fields as shown above.
- For more details, see the code in the `Routes/` directory.
