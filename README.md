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

## 🤖 AI Chatbot Features

The backend includes an AI-powered chatbot with advanced prompt engineering, agent capabilities, and comprehensive logging.

### Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  React Frontend │────▶│  Node.js API    │────▶│  Flask AI Server│
│  (Port 5173)    │     │  (Port 5000)    │     │  (Port 5001)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │                        │
                               ▼                        ▼
                        ┌─────────────┐          ┌─────────────┐
                        │ PostgreSQL  │          │ DeepSeek LLM│
                        │  Database   │          │    API      │
                        └─────────────┘          └─────────────┘
```

### AI Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/ai-chat` | Send message to AI chatbot |

#### 🔸 POST `/api/users/ai-chat`

**Request Body:**
```json
{
  "message": "What Python courses do you have?",
  "email": "user@example.com",
  "username": "user1",
  "context": [
    {"role": "user", "text": "Previous message"},
    {"role": "assistant", "text": "Previous response"}
  ],
  "prompt_type": "improved"
}
```

**Response:**
```json
{
  "reply": "AI response with markdown formatting...",
  "actions": [
    {
      "type": "ADD_TO_CART",
      "course_title": "Python for Beginners",
      "executed": true
    }
  ]
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | string | Yes | User's question or command |
| `email` | string | No | User's email for personalization |
| `username` | string | No | User's username |
| `context` | array | No | Previous conversation history |
| `prompt_type` | string | No | "naive" or "improved" (default: "improved") |

---

### Prompt Engineering Patterns

The AI uses multiple prompt engineering techniques in the Improved prompt:

#### Basic Patterns

| Pattern | Location in Prompt | Description |
|---------|-------------------|-------------|
| **Role-Based** | `=== ROLE-BASED PATTERN ===` | Defines AI as "LearnHub AI, an advanced assistant" |
| **Instructional** | `=== INSTRUCTIONAL PATTERN ===` | 5 clear rules for behavior |
| **Constraint** | Rules 1-3 | "MUST only use course titles from JSON" |
| **Structured Output** | Examples 1-3 | Markdown tables for comparisons/paths |
| **Persona Details** | `=== PERSONA DETAILS PATTERN ===` | Personality traits, communication style |
| **Error Handling** | `=== ERROR HANDLING PATTERN ===` | 4 graceful fallback scenarios |

#### Advanced Techniques

| Technique | Location in Prompt | Description |
|-----------|-------------------|-------------|
| **Few-Shot Prompting** | Examples 1, 2, 3 | Complete input/output examples |
| **Chain-of-Thought (CoT)** | `=== CHAIN-OF-THOUGHT PATTERN ===` | 4-step reasoning: UNDERSTAND → ANALYZE → REASON → RESPOND |

---

### Naive vs Improved Prompts

Toggle between prompt modes to demonstrate prompt engineering effectiveness:

#### Naive Prompt (2 lines)
```
You are a basic assistant.
Rules:
- Give very short answers (2-3 sentences maximum)
- Do NOT use markdown, tables, bullet points, or any formatting
- Do NOT use emojis
- Do NOT give recommendations or suggestions
- Do NOT explain your reasoning
- Just answer the question directly in plain text
```

#### Improved Prompt (~250 lines)
Contains all 8 patterns/techniques listed above plus:
- 3 few-shot examples with complete responses
- Ethical safeguards section
- Agent action definitions with trigger phrases

#### Context Strategy Difference

| Aspect | Naive | Improved |
|--------|-------|----------|
| **System Prompt** | 2 lines | ~250 lines |
| **Data Sent** | Course titles only (plain text) | Full JSON with all details |
| **User Context** | No cart, no enrolled courses | Cart, enrolled courses, tasks |
| **Output Format** | Plain text only | Markdown tables, emojis, structure |

---

### Agent Capabilities (4 Actions)

The AI can perform intelligent actions on behalf of the user:

#### 1. ADD_TO_CART
**Trigger Phrases:**
- "add [course] to cart"
- "add [course] to my cart"
- "I want to buy [course]"
- "enroll me in [course]"
- "purchase [course]"

**Action Format in Response:**
```
ACTIONS:
[ACTION:ADD_TO_CART]
COURSE_TITLE: Python for Beginners
[/ACTION:ADD_TO_CART]
```

#### 2. RECOMMEND_COURSES
**Trigger Phrases:**
- "recommend courses"
- "what should I learn"
- "suggest courses"
- "what courses are good for me"

**Output:** Personalized recommendations based on user's enrolled courses

#### 3. CREATE_LEARNING_PATH
**Trigger Phrases:**
- "create a learning path for [career goal]"
- "how do I become a [role]"
- "plan my learning for [skill]"

**Output:** Multi-phase markdown table with courses, duration, price, summary

#### 4. COMPARE_COURSES
**Trigger Phrases:**
- "compare [course1] and [course2]"
- "difference between [course1] and [course2]"
- "which is better: [course1] or [course2]"

**Output:** Side-by-side comparison table with all course attributes

---

### Ethical Safeguards

Built-in ethical guidelines in the Improved prompt:

| Safeguard | Description |
|-----------|-------------|
| **Honesty & Transparency** | Never make false claims; admit when unsure |
| **User Privacy & Safety** | Never ask for passwords, payment details, SSN |
| **Harmful Content Prevention** | Refuse illegal/harmful requests politely |
| **Fair & Unbiased Recommendations** | Recommend based on user needs, not hidden agendas |
| **Respect & Inclusivity** | Treat all users with respect; use inclusive language |

---

### Conversation Logging

All conversations are logged to `Python-app/conversation_logs/chat_logs.jsonl`

**Log Entry Format:**
```json
{
  "timestamp": "2026-01-11T18:30:00.000000",
  "conversation_id": "abc123-def456",
  "user_email": "user@example.com",
  "user_name": "user1",
  "user_message": "What Python courses do you have?",
  "assistant_response": "Here are the Python courses...",
  "agent_actions": [
    {"type": "RECOMMEND_COURSES", "executed": true}
  ],
  "model": "deepseek-chat",
  "tokens_used": null,
  "status": "success",
  "error": null
}
```

**Log Analysis Scripts:**
- `analyze_logs.py` - Generate statistics from logs
- `view_logs.py` - Pretty-print recent conversations

---

### Flask AI Server

**Location:** `Python-app/app.py`

**Start Server:**
```bash
cd Python-app
python app.py
```

**Server Details:**
- **Port:** 5001
- **Endpoints:** `/chat` (POST), `/health` (GET)
- **LLM:** DeepSeek Chat API
- **Environment Variables:** `DEEPSEEK_API_KEY` in `.env`

**Key Functions:**

| Function | Description |
|----------|-------------|
| `build_messages()` | Constructs message array for LLM with prompt selection |
| `call_llm()` | Sends request to DeepSeek API |
| `parse_actions()` | Extracts agent actions from LLM response |
| `log_conversation()` | Writes to JSONL log file |
| `recommend_courses()` | Course recommendation engine |
| `create_learning_path()` | Learning path generator |
| `compare_courses()` | Course comparison engine |

---

### Environment Variables

**Python-app/.env:**
```
DEEPSEEK_API_KEY=your_api_key_here
```

**Root .env:**
```
FLASK_URL=http://localhost:5001/chat
```

---

## 📝 Notes
- All endpoints return errors in the format: `{ "error": "message" }` on failure.
- All endpoints require the appropriate fields as shown above.
- For more details, see the code in the `Routes/` directory.
