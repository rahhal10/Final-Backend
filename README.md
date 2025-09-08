# Final-Backend

---

# Backend Documentation

## General Structure
- `db.js`: Database connection setup using PostgreSQL and dotenv for environment variables.
- `Server.js`: Main server file, sets up Express app, middleware, and mounts user/admin routes.
- `Routes/user.js`: All user (student) endpoints.
- `Routes/admin.js`: All admin endpoints.

---

## Database Connection (`db.js`)
**Code Explanation:**
- `import express from 'express';`  
- `import pg from 'pg';`  
	Imports PostgreSQL client library.
- `import dotenv from 'dotenv';`  
	Imports dotenv for environment variable management.
- `dotenv.config();`  
	Loads environment variables from `.env` file.
- `const pgClient = new pg.Client(process.env.DATABASE_URL);`  
	Creates a new PostgreSQL client using the database URL from environment variables.
- `export default pgClient;`  
	Exports the database client for use in other files.

---

## Server Setup (`Server.js`)
**Code Explanation:**
- `import express from 'express'`  
	Imports Express framework.
- `import dotenv from 'dotenv';`  
	Imports dotenv for environment variables.
- `import pgClient from './db.js';`  
	Imports the PostgreSQL client.
- `import UserRoutes from './Routes/user.js';`  
	Imports user routes.
- `import AdminRoutes from './Routes/admin.js';`  
	Imports admin routes.
- `import morgan from 'morgan';`  
	Imports morgan for HTTP request logging.
- `import cors from 'cors';`  
	Imports CORS middleware.
- `const app = express();`  
	Creates an Express app instance.
- `dotenv.config();`  
	Loads environment variables.
- `app.use(express.json());`  
	Enables JSON body parsing.
- `app.use(cors());`  
	Enables CORS for all routes.
- `app.use(morgan('dev'));`  
	Enables HTTP request logging in dev format.
- `app.use('/api/users', UserRoutes);`  
	Mounts user routes at `/api/users`.
- `app.use('/api/admin', AdminRoutes);`  
	Mounts admin routes at `/api/admin`.
- `pgClient.connect().then(() => { ... })`  
	Connects to the database, then starts the server on the specified port.

---

## Admin Endpoints (`Routes/admin.js`)

### 1. Get User Count
**GET** `http://localhost:5000/api/admin/usercount`
- Returns the total number of users.

### 2. Get Courses Count
**GET** `http://localhost:5000/api/admin/coursescount`
- Returns the total number of courses.

### 3. Get All Courses (Summary)
**GET** `http://localhost:5000/api/admin/admincourses`
- Returns id, title, description, and instructor for all courses.

### 4. Delete Course
**DELETE** `http://localhost:5000/api/admin/deladmincourses`
- Deletes a course by id. Request body: `{ id }`.

### 5. Edit Course Instructor
**PUT** `http://localhost:5000/api/admin/editadmincourse`
- Updates the instructor for a course. Request body: `{ id, instructor }`.

### 6. Add New Course
**POST** `http://localhost:5000/api/admin/addadmincourse`
- Adds a new course. Request body: `{ title, description, instructor, rating, duration, lessonsCount, price, imageUrl, category }`.

### 7. Get All Users
**GET** `http://localhost:5000/api/admin/adminusers`
- Returns all users.

### 8. Add New User
**POST** `http://localhost:5000/api/admin/addadminuser`
- Adds a new user. Request body: `{ email, username, password, role }`.

### 9. Delete User
**DELETE** `http://localhost:5000/api/admin/deluser`
- Deletes a user by id. Request body: `{ id }`.

---

## User Endpoints (`Routes/user.js`)

### 1. Get All Courses
**GET** `http://localhost:5000/api/users/courses`
- Returns all available courses.

### 2. Get User's Enrolled Courses
**POST** `http://localhost:5000/api/users/user-courses`
- Returns all courses a user is enrolled in. Request body: `{ email, username }`.

### 3. User Login
**POST** `http://localhost:5000/api/users/Login`
- Authenticates user. Request body: `{ email, password }`. Returns `{ role, username }`.

### 4. Add Course to Cart
**POST** `http://localhost:5000/api/users/addCart`
- Adds a course to the user's cart. Request body: `{ username, email, title, description, instructor, price, category, duration, lessons_count, rating, image_url, quantity }`.

### 5. Show Cart
**POST** `http://localhost:5000/api/users/showcart`
- Returns all items in the user's cart. Request body: `{ email }`.

### 6. Delete Item from Cart
**DELETE** `http://localhost:5000/api/users/delcart`
- Deletes an item from the cart by id. Request body: `{ id }`.

### 7. Update Cart Quantity
**PUT** `http://localhost:5000/api/users/updatecartquantity`
- Updates the quantity of a cart item. Request body: `{ id, quantity }`.

### 8. Enroll in a Course
**POST** `http://localhost:5000/api/users/addcoursestouser`
- Enrolls a user in a course. Request body: `{ username, email, title, description, instructor, price, category, duration, lessons_count, rating, image_url }`.

### 9. Get Assignments
**GET** `http://localhost:5000/api/users/assignments`
- Returns all assignments (tasks).

### 10. User Signup
**POST** `http://localhost:5000/api/users/signup`
- Registers a new user. Request body: `{ username, email, password, role }`.

---

# Endpoint Code Explanations

## Example: Admin Endpoint - Delete Course
```js
AdminRoutes.delete('/deladmincourses', async (req, res) => {
		const { id } = req.body; // Get course id from request
		if (!id) {
				return res.status(400).json({ error: 'ID is required.' }); // Validate input
		}
		try {
				const query = 'DELETE FROM courses WHERE id = $1 RETURNING *'; // SQL delete
				const result = await pgClient.query(query, [id]);
				if (result.rowCount === 0) {
						return res.status(404).json({ error: 'Course not found.' }); // Not found
				}
				return res.json({ deleted: result.rows[0] }); // Success
		} catch (err) {
				console.error(err);
				return res.status(500).json({ error: 'Server error.' }); // Error
		}
});
```
**Line-by-line explanation:**
- Defines a DELETE endpoint `/deladmincourses`.
- Extracts `id` from request body.
- Validates that `id` is provided.
- Tries to delete the course with the given id from the database.
- Returns 404 if not found, or the deleted course if successful.
- Handles errors and returns 500 if something goes wrong.

---

## (Repeat similar code explanations for each endpoint as needed)



---

## Endpoint: Get User Count
**Route:** `GET /usercount`

**Description:**
Returns the total number of users in the system. Used by admin to see how many users are registered.

**Code Explanation:**
- `AdminRoutes.get('/usercount', async (req, res) => {`  
	Defines a GET endpoint `/usercount` for the admin router.
- `try {`  
	Starts a try block to handle potential errors.
- `const result = await pgClient.query('SELECT COUNT(*) FROM users');`  
	Executes a SQL query to count all users in the `users` table.
- `return res.json({ count: result.rows[0].count });`  
	Sends the count as a JSON response.
- `} catch (err) {`  
	Catches any errors that occur during the query.
- `console.error(err);`  
	Logs the error to the console.
- `return res.status(500).json({ error: 'Server error.' });`  
	Sends a 500 error response if something goes wrong.
- `});`  
	Closes the endpoint definition.

---

## Endpoint: Get All Users
**Route:** `GET /adminusers`

**Description:**
Fetches all users from the `users` table and returns them to the admin.

**Code Explanation:**
- `AdminRoutes.get('/adminusers', async (req, res) => {`  
	Defines a GET endpoint `/adminusers` for the admin router.
- `try {`  
	Starts a try block to handle potential errors.
- `const result = await pgClient.query('SELECT * FROM users');`  
	Executes a SQL query to select all users from the `users` table.
- `return res.json(result.rows);`  
	Sends the array of user objects as a JSON response.
- `} catch (err) {`  
	Catches any errors that occur during the query.
- `console.error(err);`  
	Logs the error to the console.
- `return res.status(500).json({ error: 'Server error.' });`  
	Sends a 500 error response if something goes wrong.
- `});`  
	Closes the endpoint definition.

---


