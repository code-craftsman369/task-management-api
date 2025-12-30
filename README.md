# 📋 Task Management REST API

Production-ready RESTful API for task management built with Flask and SQLite, featuring comprehensive CRUD operations, advanced filtering, and an interactive web dashboard.

![Task Management API](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### Core Functionality
- ✅ **CRUD Operations**: Create, Read, Update, Delete tasks
- ✅ **Status Management**: Toggle task completion status
- ✅ **Batch Operations**: Delete all tasks at once

### Advanced Features
- 🔍 **Search**: Full-text search across title and description
- 🎯 **Filtering**: Filter by status (completed/incomplete) and priority levels
- 📊 **Sorting**: Sort by creation date, priority, or deadline
- ⏰ **Deadline Tracking**: Set and track task deadlines
- ⚠️ **Overdue Detection**: Automatic detection of overdue tasks
- 💾 **Data Persistence**: JSON-based data storage

## 🛠️ Tech Stack

- **Backend**: Python 3.13 + Flask 3.1
- **Database**: JSON file storage (easily upgradeable to SQLite/PostgreSQL)
- **API Design**: RESTful principles
- **Frontend**: HTML5 + Vanilla JavaScript (Single Page Application)

## 📦 Installation
```bash
# Clone repository
git clone https://github.com/code-craftsman369/task-management-api.git
cd task-management-api

# Install dependencies
pip install flask

# Run server
python app.py
```

Server starts at `http://localhost:5001`

## 📖 API Documentation

### 1. Create Task

**POST** `/tasks`
```bash
curl -X POST http://localhost:5001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API docs",
    "priority": "high",
    "deadline": "2025-12-31T18:00:00"
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API docs",
  "completed": false,
  "priority": "high",
  "deadline": "2025-12-31T18:00:00",
  "created_at": "2025-12-30T10:00:00.000000",
  "updated_at": "2025-12-30T10:00:00.000000"
}
```

### 2. Get All Tasks

**GET** `/tasks`

#### Basic retrieval
```bash
curl http://localhost:5001/tasks
```

#### Search
```bash
curl "http://localhost:5001/tasks?search=documentation"
```

#### Filter by status
```bash
# Completed tasks
curl "http://localhost:5001/tasks?status=completed"

# Incomplete tasks
curl "http://localhost:5001/tasks?status=incomplete"
```

#### Filter by priority
```bash
curl "http://localhost:5001/tasks?priority=high"
```

#### Sort
```bash
# By priority (descending)
curl "http://localhost:5001/tasks?sort_by=priority&order=desc"

# By deadline (ascending)
curl "http://localhost:5001/tasks?sort_by=deadline&order=asc"

# By creation date (descending)
curl "http://localhost:5001/tasks?sort_by=created_at&order=desc"
```

#### Combined queries
```bash
# High priority + sorted by deadline
curl "http://localhost:5001/tasks?priority=high&sort_by=deadline&order=asc"
```

### 3. Get Single Task

**GET** `/tasks/{id}`
```bash
curl http://localhost:5001/tasks/1
```

### 4. Update Task

**PUT** `/tasks/{id}`
```bash
curl -X PUT http://localhost:5001/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated task title",
    "completed": true,
    "deadline": "2025-12-31T18:00:00"
  }'
```

### 5. Toggle Task Status

**PATCH** `/tasks/{id}/toggle`
```bash
curl -X PATCH http://localhost:5001/tasks/1/toggle
```

### 6. Delete Task

**DELETE** `/tasks/{id}`
```bash
curl -X DELETE http://localhost:5001/tasks/1
```

### 7. Delete All Tasks

**DELETE** `/tasks/all`
```bash
curl -X DELETE http://localhost:5001/tasks/all
```

### 8. Get Overdue Tasks

**GET** `/tasks/overdue`
```bash
curl http://localhost:5001/tasks/overdue
```

## 📊 Data Structure

### Task Object
```json
{
  "id": 1,
  "title": "Task title",
  "description": "Task description (optional)",
  "completed": false,
  "priority": "medium",
  "deadline": "2025-12-31T18:00:00",
  "created_at": "2025-12-30T10:00:00.000000",
  "updated_at": "2025-12-30T10:00:00.000000"
}
```

### Field Descriptions

| Field | Type | Required | Description | Default |
|-------|------|----------|-------------|---------|
| `id` | int | - | Auto-generated ID | - |
| `title` | string | ✓ | Task title | - |
| `description` | string | - | Task description | "" |
| `completed` | boolean | - | Completion status | false |
| `priority` | string | - | Priority (high/medium/low) | "medium" |
| `deadline` | string | - | Deadline (ISO 8601 format) | null |
| `created_at` | string | - | Creation timestamp | Auto-set |
| `updated_at` | string | - | Last update timestamp | Auto-set |

## 🎯 Use Cases

### Use Case 1: Get Today's Priority Tasks
```bash
curl "http://localhost:5001/tasks?priority=high&sort_by=deadline&order=asc"
```

### Use Case 2: Check Overdue Tasks
```bash
curl http://localhost:5001/tasks/overdue
```

### Use Case 3: Search for Specific Keywords
```bash
curl "http://localhost:5001/tasks?search=meeting"
```

## 💾 Data Storage

Task data is stored in `tasks.json` file and persists across server restarts.

## 🌐 Web Dashboard

Access the interactive web dashboard at `http://localhost:5001` after starting the server.

Features:
- ✅ Add, edit, and delete tasks
- ✅ Filter by status and priority
- ✅ Search functionality
- ✅ Sort by various criteria
- ✅ Responsive design

## 🧪 Testing

### Create Test Data
```bash
# High priority with deadline
curl -X POST http://localhost:5001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Prepare presentation",
    "description": "Sales meeting next week",
    "priority": "high",
    "deadline": "2025-12-15T17:00:00"
  }'

# Medium priority with deadline
curl -X POST http://localhost:5001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Submit monthly report",
    "description": "October sales report",
    "priority": "medium",
    "deadline": "2025-12-20T12:00:00"
  }'
```

## 🛣️ Roadmap

- [ ] SQLite/PostgreSQL database integration
- [ ] User authentication (JWT)
- [ ] Task categories/tags
- [ ] Recurring tasks
- [ ] Email notifications
- [ ] Docker containerization
- [ ] API rate limiting
- [ ] Comprehensive test suite

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 👤 Author

**Tatsu**  
GitHub: [@code-craftsman369](https://github.com/code-craftsman369)  
X: [@web3_builder369](https://twitter.com/web3_builder369)

---

⭐ If you find this project useful, please consider giving it a star!