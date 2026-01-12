import os
import json
import requests
from pathlib import Path
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(Path(__file__).parent / "flask.env")

app = Flask(__name__)

API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
API_URL = os.getenv("DEEPSEEK_API_URL", "").strip()
MODEL = os.getenv("DEEPSEEK_MODEL", "").strip()
TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))
MAX_CHARS = int(os.getenv("MAX_DB_CHARS", "12000"))

LOGS_DIR = Path(__file__).parent / "conversation_logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE = LOGS_DIR / "chat_logs.jsonl"

def log_conversation(log_data):
    """Log conversation data to JSONL file"""
    try:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_email": log_data.get("user_email", ""),
            "user_name": log_data.get("user_name", ""),
            "user_prompt": log_data.get("user_prompt", ""),
            "db_context_summary": log_data.get("db_context_summary", {}),
            "model_response": log_data.get("model_response", ""),
            "agent_actions": log_data.get("agent_actions", []),
            "status": log_data.get("status", "success"),
            "error": log_data.get("error", None)
        }
        
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Error logging conversation: {e}")

# NAIVE PROMPT: Basic prompt with minimal instructions (for AB testing comparison)
NAIVE_SYSTEM_PROMPT = """
You are a basic assistant.
Rules:
- Give very short answers (2-3 sentences maximum)
- Do NOT use markdown, tables, bullet points, or any formatting
- Do NOT use emojis
- Do NOT give recommendations or suggestions
- Do NOT explain your reasoning
- Just answer the question directly in plain text
""".strip()

# IMPROVED PROMPT: Advanced prompt with role-based, CoT, few-shot, and structured output patterns
IMPROVED_SYSTEM_PROMPT = """
=== ROLE-BASED PATTERN: Persona Definition ===
You are LearnHub AI, an advanced assistant for an e-learning website with sophisticated agent capabilities.

=== PERSONA DETAILS PATTERN: Personality & Communication Style ===
Your personality traits:
- Friendly and encouraging: You celebrate user progress and motivate learning
- Expert advisor: You have deep knowledge of all courses and career paths
- Proactive helper: You anticipate user needs and offer relevant suggestions
- Clear communicator: You explain complex topics simply and use visual formatting

Communication style:
- Use emojis sparingly but effectively (🎯, 📚, 🚀, ✅)
- Be concise but thorough
- Always end with a helpful follow-up question or suggestion
- Use markdown formatting for better readability

=== CHAIN-OF-THOUGHT PATTERN: Step-by-Step Reasoning ===
When answering complex questions, think through these steps:
1. UNDERSTAND: What is the user actually asking for?
2. ANALYZE: What relevant data do I have in the JSON?
3. REASON: How can I best help based on their enrolled courses, cart, and goals?
4. RESPOND: Provide a clear, structured answer with actionable next steps

=== DATA CONTEXT ===
You are given database data in JSON with these keys:
- courses: list of matching courses from the catalog search
- user_course: courses the user is enrolled in (if provided)
- cart_products: courses in the user cart (if provided)
- tasks: tasks (may be empty)

=== INSTRUCTIONAL PATTERN: Rules & Guidelines ===
Rules:
1) When recommending or listing courses, you MUST only use course titles that appear in the provided JSON (courses, user_course, cart_products).
2) If the database data is empty or insufficient, do NOT invent course titles. Instead:
   - Ask 1-2 short questions to narrow down what the user wants, OR
   - Suggest categories/skills generally (no course names) and explain you need more data to recommend specific courses.
3) If the user asks for "random courses" or "suggest something interesting", randomly pick 3-6 courses FROM THE JSON data (only real DB courses). If JSON has no courses, say the catalog search returned none and ask what topic they want.
4) Keep the response natural like a normal chatbot (DeepSeek style), not robotic, and avoid repeating "provided data".
5) Format: short intro + bullet list of courses (Title - duration, lessons, rating, price if available) + one short follow-up question.

=== ERROR HANDLING PATTERN: Graceful Fallbacks ===
Handle edge cases gracefully:
- If a course is not found: "I couldn't find that exact course. Did you mean [similar course]? Or would you like me to search for something else?"
- If user request is unclear: "I'd love to help! Could you tell me more about [specific question]?"
- If no courses match criteria: "I don't see courses matching that criteria right now. Here are some popular alternatives: [list alternatives]"
- If action fails: "I encountered an issue with that request. Let me try a different approach..."

=== ETHICAL SAFEGUARDS ===
You must follow these ethical guidelines at all times:

1) HONESTY & TRANSPARENCY:
   - Never make false claims about courses, prices, or features
   - If you don't know something, say so honestly
   - Don't pretend to have capabilities you don't have

2) USER PRIVACY & SAFETY:
   - Never ask for sensitive personal information (passwords, payment details, SSN)
   - Don't store or reference personal data beyond the current session
   - Respect user boundaries and preferences

3) HARMFUL CONTENT PREVENTION:
   - Refuse requests for illegal, harmful, or unethical content
   - Don't provide advice that could cause financial, physical, or emotional harm
   - Politely decline inappropriate requests with: "I'm sorry, I can't help with that request."

4) FAIR & UNBIASED RECOMMENDATIONS:
   - Recommend courses based on user needs, not hidden agendas
   - Present balanced comparisons without unfair bias
   - Disclose if recommendations are based on limited data

5) RESPECT & INCLUSIVITY:
   - Treat all users with respect regardless of background
   - Use inclusive language
   - Avoid stereotypes or discriminatory assumptions

The data structure:
"courses": All available courses on the platform (NOT the user's enrolled courses),
"user_course": Courses the user is currently enrolled in (their dashboard/enrolled courses),
"cart_products": Courses in the user's shopping cart,
"tasks": Assignments and tasks,

When the user asks about "my courses", "enrolled courses", or "dashboard courses", use ONLY the "user_course" data.
When asked about available courses, recommendations, or browsing, use the "courses" data.

ADVANCED AGENT CAPABILITIES:
You can perform multiple types of intelligent actions on behalf of the user:

1) ADD TO CART:
Trigger phrases:
- "add [course] to cart"
- "add [course] to my cart"
- "I want to buy [course]"
- "enroll me in [course]"
- "purchase [course]"

When adding a course to cart, show the course details in a nice format:

**🛒 Adding to Cart**

| Course | Duration | Lessons | Rating | Price |
|--------|----------|---------|--------|-------|
| Course Name | X weeks | X | X/5.0 | $X.XX |

Then include the action at the end:

ACTIONS:
[ACTION:ADD_TO_CART]
COURSE_TITLE: <exact course title from database>
[/ACTION:ADD_TO_CART]

2) COURSE RECOMMENDATIONS:
Trigger phrases:
- "recommend courses for me"
- "what courses should I take"
- "suggest courses based on my profile"
- "personalized recommendations"

When user asks for recommendations, generate them using this markdown format:

**🎯 Personalized Course Recommendations**

Based on your enrolled courses, here are my top picks:

| Course | Category | Duration | Rating | Price | Why Recommended |
|--------|----------|----------|--------|-------|-----------------|
| Course Name | Category | X weeks | X/5.0 | $X.XX | Brief reason |

**💡 Top Pick:** [Course name] - [reason why it's the best choice]

3) LEARNING PATH PLANNER:
Trigger phrases:
- "create a learning path for [career goal]"
- "plan my studies for [career goal]"
- "what should I learn to become [career goal]"
- "career roadmap for [career goal]"

When user asks for a learning path, generate it using this markdown format:

**🗺️ Learning Path: [Career Goal]**

**Phase 1: Foundation**
| Course | Duration | Lessons | Rating | Price |
|--------|----------|---------|--------|-------|
| Course Name | X weeks | X | X/5.0 | $X.XX |

**Phase 2: Intermediate**
| Course | Duration | Lessons | Rating | Price |
|--------|----------|---------|--------|-------|
| Course Name | X weeks | X | X/5.0 | $X.XX |

**Phase 3: Advanced**
| Course | Duration | Lessons | Rating | Price |
|--------|----------|---------|--------|-------|
| Course Name | X weeks | X | X/5.0 | $X.XX |

**📊 Summary:** Total duration, total cost, and key benefits.

4) COURSE COMPARISON:
When user asks to compare courses, generate a comparison table using markdown format:

**📊 Course Comparison**

| Feature | Course 1 | Course 2 |
|---------|----------|----------|
| Category | value | value |
| Duration | value | value |
| Lessons | value | value |
| Rating | value | value |
| Price | value | value |

**🏆 Recommendation:** [Your recommendation based on the comparison]

CRITICAL RULES:
- When triggered, you MUST include the ACTIONS section at the END of your response
- Do NOT ask for confirmation - just execute and confirm it's done
- Course titles must exactly match titles from the database JSON
- For learning paths, extract the career goal clearly
- For course comparisons, generate the table directly in your response (no action needed)

Example 1 - User: "recommend courses for me"
Response: "Based on your enrolled courses, I'll find personalized recommendations for you!

ACTIONS:
[ACTION:RECOMMEND_COURSES]
[/ACTION:RECOMMEND_COURSES]"

Example 2 - User: "create a learning path for web development"
Response: "Here's your personalized learning path for web development:

**🗺️ Learning Path: Web Development**

**Phase 1: Foundation**
| Course | Duration | Lessons | Rating | Price |
|--------|----------|---------|--------|-------|
| Python for Beginners | 5 weeks | 20 | 4.9/5.0 | $24.99 |
| Complete Web Development Bootcamp | 10 weeks | 40 | 4.9/5.0 | $49.99 |

**Phase 2: Backend Development**
| Course | Duration | Lessons | Rating | Price |
|--------|----------|---------|--------|-------|
| Node.js Backend Development | 6 weeks | 24 | 4.8/5.0 | $34.99 |
| Database Design & SQL | 5 weeks | 20 | 4.6/5.0 | $26.99 |

**Phase 3: DevOps & Deployment**
| Course | Duration | Lessons | Rating | Price |
|--------|----------|---------|--------|-------|
| DevOps Engineering | 7 weeks | 24 | 4.7/5.0 | $35.99 |
| Cloud Computing with AWS | 7 weeks | 24 | 4.8/5.0 | $36.99 |

**📊 Summary:** ~40 weeks total, ~$210 investment. This path takes you from beginner to deployment-ready full-stack developer!"

Example 3 - User: "compare DevOps and Cloud Computing courses"
Response: "Here's a detailed comparison of these courses:

**📊 Course Comparison**

| Feature | DevOps Engineering | Cloud Computing with AWS |
|---------|-------------------|-------------------------|
| Category | DevOps | Cloud |
| Duration | 7 weeks | 7 weeks |
| Lessons | 24 | 24 |
| Rating | 4.7/5.0 | 4.8/5.0 |
| Price | $35.99 | $36.99 |

**🏆 Recommendation:** Both courses are excellent! Cloud Computing has a slightly higher rating (4.8 vs 4.7), while DevOps is $1 cheaper. They complement each other well."

If the answer is not present in the data, say you couldn't find it. Be concise and accurate.
""".strip()

SYSTEM_PROMPT = IMPROVED_SYSTEM_PROMPT

def build_messages(user_input, db_data, context=None, prompt_type="improved"):
    def compact_courses(items):
        out = []
        for c in items or []:
            out.append({
                "title": c.get("title"),
                "category": c.get("category"),
                "duration": c.get("duration"),
                "lessons_count": c.get("lessons_count"),
                "rating": c.get("rating"),
                "price": c.get("price"),
                "instructor": c.get("instructor"),
            })
        return out

    context = context or []
    context_data = {
        "courses": compact_courses(db_data.get("courses", [])),
        "user_course": compact_courses(db_data.get("user_course", [])),
        "cart_products": compact_courses(db_data.get("cart_products", [])),
        "tasks": db_data.get("tasks", []),
    }

    db_text = json.dumps(context_data, ensure_ascii=False, indent=2)
    if len(db_text) > MAX_CHARS:
        db_text = db_text[:MAX_CHARS] + "\n... (truncated)"

    selected_prompt = IMPROVED_SYSTEM_PROMPT if prompt_type == "improved" else NAIVE_SYSTEM_PROMPT
    messages = [{"role": "system", "content": selected_prompt}]

    for message in context:
        messages.append({
            "role": message.get("role", "user"),
            "content": message.get("text", message.get("content", ""))
        })

    if prompt_type == "improved":
        messages.append({
            "role": "user",
            "content": f"User message:\n{user_input}\n\nDatabase JSON:\n{db_text}"
        })
    else:
        course_titles = [c.get("title", "") for c in context_data.get("courses", [])]
        simple_context = ", ".join(course_titles[:10]) if course_titles else "No courses available"
        messages.append({
            "role": "user",
            "content": f"{user_input}\n\nAvailable courses: {simple_context}"
        })

    return messages

def recommend_courses(user_courses, all_courses, user_input):
    """Course Recommendation Engine - Personalized suggestions based on user's enrolled courses"""
    try:
        user_categories = set()
        user_instructors = set()
        user_levels = []
        
        for course in user_courses:
            if course.get('category'):
                user_categories.add(course['category'].lower())
            if course.get('instructor'):
                user_instructors.add(course['instructor'].lower())
            title = course.get('title', '').lower()
            if any(word in title for word in ['beginner', 'intro', 'basic']):
                user_levels.append('beginner')
            elif any(word in title for word in ['advanced', 'master', 'expert']):
                user_levels.append('advanced')
            else:
                user_levels.append('intermediate')
        
        recommendations = []
        for course in all_courses:
            if any(uc.get('title') == course.get('title') for uc in user_courses):
                continue
            
            score = 0
            reasons = []
            
            course_category = course.get('category', '').lower()
            if course_category in user_categories:
                score += 3
                reasons.append(f"Similar to your {course_category} courses")
            
            course_instructor = course.get('instructor', '').lower()
            if course_instructor in user_instructors:
                score += 2
                reasons.append(f"Same instructor as your other courses")
            
            if user_levels:
                avg_level = max(set(user_levels), key=user_levels.count)
                course_title = course.get('title', '').lower()
                if avg_level == 'beginner' and any(word in course_title for word in ['intermediate', 'advanced']):
                    score += 2
                    reasons.append("Good next step for your level")
                elif avg_level == 'intermediate' and any(word in course_title for word in ['advanced', 'master']):
                    score += 2
                    reasons.append("Advanced course for your experience")
            
            if course.get('rating', 0) >= 4.5:
                score += 1
                reasons.append("Highly rated course")
            
            if score >= 2:
                recommendations.append({
                    'course': course,
                    'score': score,
                    'reasons': reasons[:2]
                })
        
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:3]
        
    except Exception as e:
        print(f"Error in recommend_courses: {e}")
        return []

def create_learning_path(user_courses, all_courses, career_goal):
    """Learning Path Planner - Creates structured learning paths for career goals"""
    try:
        career_paths = {
            'web development': ['web development', 'javascript', 'react', 'node.js', 'html', 'css', 'frontend', 'backend'],
            'data science': ['data science', 'python', 'machine learning', 'statistics', 'analysis'],
            'mobile development': ['mobile', 'ios', 'android', 'react native', 'flutter'],
            'devops': ['devops', 'docker', 'kubernetes', 'aws', 'cloud', 'deployment'],
            'ui/ux design': ['design', 'ui', 'ux', 'figma', 'photoshop', 'user experience']
        }
        
        career_goal_lower = career_goal.lower()
        relevant_path = None
        for path, keywords in career_paths.items():
            if any(keyword in career_goal_lower for keyword in keywords):
                relevant_path = path
                break
        
        if not relevant_path:
            relevant_path = 'web development'
        
        relevant_categories = career_paths[relevant_path]
        relevant_courses = []
        
        for course in all_courses:
            course_category = course.get('category', '').lower()
            course_title = course.get('title', '').lower()
            
            if any(cat in course_category or cat in course_title for cat in relevant_categories):
                if any(word in course_title for word in ['beginner', 'intro', 'basic']):
                    level = 'beginner'
                elif any(word in course_title for word in ['advanced', 'master', 'expert']):
                    level = 'advanced'
                else:
                    level = 'intermediate'
                
                relevant_courses.append({
                    'course': course,
                    'level': level,
                    'relevance_score': sum(1 for cat in relevant_categories if cat in course_category or cat in course_title)
                })
        
        relevant_courses.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        learning_path = {
            'career_goal': career_goal,
            'path_name': relevant_path.title(),
            'steps': []
        }
        
        beginner_courses = [c for c in relevant_courses if c['level'] == 'beginner'][:2]
        intermediate_courses = [c for c in relevant_courses if c['level'] == 'intermediate'][:2]
        advanced_courses = [c for c in relevant_courses if c['level'] == 'advanced'][:2]
        
        step_num = 1
        for level, courses in [('Foundation', beginner_courses), ('Intermediate', intermediate_courses), ('Advanced', advanced_courses)]:
            if courses:
                learning_path['steps'].append({
                    'step': step_num,
                    'level': level,
                    'courses': [c['course'] for c in courses],
                    'description': f"Build {level.lower()} skills in {relevant_path.title()}"
                })
                step_num += 1
        
        return learning_path
        
    except Exception as e:
        print(f"Error in create_learning_path: {e}")
        return None

def compare_courses(course_titles, all_courses):
    """Course Comparison Tool - Creates detailed comparison of multiple courses"""
    try:
        print(f"compare_courses called with titles: {course_titles}")
        print(f"Available courses: {[c.get('title') for c in all_courses]}")
        
        found_courses = []
        for title in course_titles:
            title_lower = title.lower().strip()
            best_match = None
            
            for course in all_courses:
                course_title = course.get('title', '').lower().strip()
                
                if course_title == title_lower:
                    best_match = course
                    break
                
                if title_lower in course_title or course_title in title_lower:
                    best_match = course
                    break
                
                title_words = set(title_lower.split())
                course_words = set(course_title.split())
                if len(title_words & course_words) >= 2:
                    best_match = course
                    break
            
            if best_match and best_match not in found_courses:
                found_courses.append(best_match)
                print(f"Matched '{title}' to '{best_match.get('title')}'")
            else:
                print(f"No match found for '{title}'")
        
        print(f"Found {len(found_courses)} courses for comparison")
        
        if len(found_courses) < 2:
            print("Not enough courses found for comparison")
            return None
        
        comparison = {
            'courses': found_courses,
            'comparison_table': {},
            'recommendations': []
        }
        
        features = ['price', 'rating', 'duration', 'instructor', 'category', 'lessons_count']
        for feature in features:
            comparison['comparison_table'][feature] = []
            for course in found_courses:
                value = course.get(feature, 'N/A')
                if feature == 'price' and value != 'N/A':
                    value = f"${value}"
                elif feature == 'rating' and value != 'N/A':
                    value = f"{value}/5.0"
                comparison['comparison_table'][feature].append(value)
        
        best_value = min(found_courses, key=lambda c: (c.get('price', float('inf')), -c.get('rating', 0)))
        
        highest_rated = max(found_courses, key=lambda c: c.get('rating', 0))
        
        most_comprehensive = max(found_courses, key=lambda c: c.get('lessons_count', 0))
        
        comparison['recommendations'] = [
            {'type': 'Best Value', 'course': best_value, 'reason': f"Lowest price at ${best_value.get('price', 0)}"},
            {'type': 'Highest Rated', 'course': highest_rated, 'reason': f"Top rating: {highest_rated.get('rating', 0)}/5.0"},
            {'type': 'Most Comprehensive', 'course': most_comprehensive, 'reason': f"Most lessons: {most_comprehensive.get('lessons_count', 0)}"}
        ]
        
        return comparison
        
    except Exception as e:
        print(f"Error in compare_courses: {e}")
        return None

def parse_actions(response_text):
    """Extract actions from LLM response"""
    actions = []
    
    if "ACTIONS:" in response_text and "[ACTION:ADD_TO_CART]" in response_text:
        try:
            action_section = response_text.split("ACTIONS:")[1]
            action_blocks = action_section.split("[ACTION:ADD_TO_CART]")
            
            for block in action_blocks[1:]:
                if "[/ACTION:ADD_TO_CART]" in block:
                    action_content = block.split("[/ACTION:ADD_TO_CART]")[0]
                    if "COURSE_TITLE:" in action_content:
                        course_title = action_content.split("COURSE_TITLE:")[1].strip()
                        actions.append({
                            "type": "ADD_TO_CART",
                            "course_title": course_title
                        })
        except Exception as e:
            print(f"Error parsing ADD_TO_CART actions: {e}")
    
    if "ACTIONS:" in response_text and "[ACTION:RECOMMEND_COURSES]" in response_text:
        try:
            action_section = response_text.split("ACTIONS:")[1]
            action_blocks = action_section.split("[ACTION:RECOMMEND_COURSES]")
            
            for block in action_blocks[1:]:
                if "[/ACTION:RECOMMEND_COURSES]" in block:
                    actions.append({
                        "type": "RECOMMEND_COURSES",
                        "executed": False  # Will be executed by backend
                    })
                    break
        except Exception as e:
            print(f"Error parsing RECOMMEND_COURSES actions: {e}")
    
    if "ACTIONS:" in response_text and "[ACTION:CREATE_LEARNING_PATH]" in response_text:
        try:
            action_section = response_text.split("ACTIONS:")[1]
            action_blocks = action_section.split("[ACTION:CREATE_LEARNING_PATH]")
            
            for block in action_blocks[1:]:
                if "[/ACTION:CREATE_LEARNING_PATH]" in block:
                    action_content = block.split("[/ACTION:CREATE_LEARNING_PATH]")[0]
                    career_goal = ""
                    if "CAREER_GOAL:" in action_content:
                        career_goal = action_content.split("CAREER_GOAL:")[1].strip()
                    actions.append({
                        "type": "CREATE_LEARNING_PATH",
                        "career_goal": career_goal,
                        "executed": False  # Will be executed by backend
                    })
                    break
        except Exception as e:
            print(f"Error parsing CREATE_LEARNING_PATH actions: {e}")
    
    if "**🗺️ Learning Path:" in response_text or "Learning Path:" in response_text:
        career_goal = ""
        if "Learning Path:" in response_text:
            try:
                start = response_text.find("Learning Path:") + len("Learning Path:")
                end = response_text.find("**", start)
                if end == -1:
                    end = response_text.find("\n", start)
                career_goal = response_text[start:end].strip()
            except:
                career_goal = "unknown"
        
        actions.append({
            "type": "CREATE_LEARNING_PATH",
            "career_goal": career_goal,
            "executed": True
        })
    
    if "**📊 Course Comparison**" in response_text or "Course Comparison" in response_text:
        actions.append({
            "type": "COMPARE_COURSES",
            "executed": True
        })
    
    return actions

def call_llm(messages):
    if not API_KEY:
        raise RuntimeError("DEEPSEEK_API_KEY missing in flask.env")

    resp = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"model": MODEL, "stream": False, "messages": messages},
        timeout=TIMEOUT
    )
    if resp.status_code != 200:
        raise RuntimeError(f"LLM HTTP {resp.status_code}: {resp.text}")

    data = resp.json()
    return data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/chat", methods=["POST"])
def chat():
    user_email = ""
    user_name = ""
    user_input = ""
    
    try:
        body = request.get_json(silent=True) or {}
        user_input = (body.get("userInput") or "").strip()
        db_data = body.get("dbData", {}) or {}
        context = body.get("context", [])  # Accept context history
        prompt_type = body.get("promptType", "improved")
        user_email = body.get("userEmail", "")
        user_name = body.get("userName", "")

        if not user_input:
            return jsonify({"error": "userInput is required"}), 400

        messages = build_messages(user_input, db_data, context, prompt_type)
        reply = call_llm(messages) or "I couldn't generate a response."
        actions = parse_actions(reply)
        executed_results = []
        for action in actions:
            if action.get("executed") == False:
                result = None
                try:
                    if action["type"] == "RECOMMEND_COURSES":
                        result = recommend_courses(
                            db_data.get("user_course", []), 
                            db_data.get("courses", []), 
                            user_input
                        )
                    elif action["type"] == "CREATE_LEARNING_PATH":
                        career_goal = action.get("career_goal", "")
                        if career_goal:
                            result = create_learning_path(
                                db_data.get("user_course", []), 
                                db_data.get("courses", []), 
                                career_goal
                            )
                    if result:
                        executed_results.append({
                            "type": action["type"],
                            "result": result,
                            "success": True
                        })
                        action["executed"] = True
                        action["result"] = result
                except Exception as e:
                    print(f"Error executing agent action {action['type']}: {e}")
                    executed_results.append({
                        "type": action["type"],
                        "error": str(e),
                        "success": False
                    })
        
        display_reply = reply.split("ACTIONS:")[0].strip() if "ACTIONS:" in reply else reply
        db_context_summary = {
            "courses_count": len(db_data.get("courses", [])),
            "user_courses_count": len(db_data.get("user_course", [])),
            "cart_items_count": len(db_data.get("cart_products", [])),
            "tasks_count": len(db_data.get("tasks", []))
        }
        
        log_conversation({
            "user_email": user_email,
            "user_name": user_name,
            "user_prompt": user_input,
            "db_context_summary": db_context_summary,
            "model_response": display_reply,
            "agent_actions": actions,
            "status": "success"
        })
        
        return jsonify({
            "reply": display_reply, 
            "actions": actions,
            "executed_results": executed_results
        })

    except Exception as e:
        log_conversation({
            "user_email": user_email,
            "user_name": user_name,
            "user_prompt": user_input,
            "db_context_summary": {},
            "model_response": "",
            "agent_actions": [],
            "status": "error",
            "error": str(e)
        })
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("FLASK_PORT", "8000")),
        debug=os.getenv("FLASK_DEBUG", "true").lower() == "true"
    )
