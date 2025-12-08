# Cbon - Project Management System

A full-stack project management application with authentication, projects, and Kanban task boards.

## Features

- 🔐 **Authentication**: JWT-based user authentication with register/login
- 📁 **Project Management**: Create, update, delete projects with UUID support
- 📋 **Kanban Board**: Drag-and-drop task management (Not Started, In Progress, Completed)
- 👥 **User Management**: User profiles and task assignment
- 🎨 **Modern UI**: Built with Vue 3, TypeScript, and Tailwind CSS v4
- ⚡ **Fast API**: FastAPI backend with PostgreSQL database

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation
- **JWT** - Authentication tokens
- **Bcrypt** - Password hashing

### Frontend
- **Vue 3** - Composition API
- **TypeScript** - Type safety
- **Pinia** - State management
- **Vue Router** - Navigation
- **Axios** - HTTP client
- **Tailwind CSS v4** - Styling

## Prerequisites

- Python 3.12+
- Node.js 18+
- Docker & Docker Compose
- uv (Python package manager)
- npm or pnpm

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Cbon
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies with uv
uv sync

# Start PostgreSQL with Docker
docker-compose up -d

# The database will be created automatically on first run
# Tables will be created when the FastAPI app starts

# Run the development server
uv run uvicorn app.main:app --reload
```

Backend will be available at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## Environment Variables

### Backend (`backend/.env`)

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cbon
DB_USER=postgres
DB_PASSWORD=postgres
```

### Frontend (`frontend/.env`)

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/refresh` - Refresh token

### Projects
- `GET /api/v1/projects` - List all projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects/{id}` - Get project by ID
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

### Tasks
- `GET /api/v1/tasks` - List all tasks
- `GET /api/v1/tasks?project_id={id}` - Get tasks for project
- `POST /api/v1/tasks` - Create task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

### Users
- `GET /api/v1/users` - List all users
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

## Database Schema

### Users
- `id` (UUID) - Primary key
- `email` (Text) - Unique
- `full_name` (Text)
- `password_hash` (Text)
- `created_at`, `updated_at` (Timestamp)

### Projects
- `id` (UUID) - Primary key
- `owner_id` (UUID) - Foreign key to users
- `title` (Text)
- `description` (Text)
- `status` (Text) - active, completed, on-hold, cancelled
- `start_date`, `due_date` (Date)
- `created_at`, `updated_at` (Timestamp)

### Tasks
- `id` (UUID) - Primary key
- `project_id` (UUID) - Foreign key to projects
- `assigned_to` (UUID) - Foreign key to users
- `title` (Text)
- `description` (Text)
- `status` (Text) - not_started, in_progress, completed, archived
- `priority` (Text) - low, medium, high
- `due_date` (Timestamp)
- `position` (Text)
- `created_at`, `updated_at` (Timestamp)

### Project Members
- `user_id` (UUID) - Foreign key to users
- `project_id` (UUID) - Foreign key to projects
- `role` (Text)
- `joined_at` (Timestamp)

## Development

### Backend Development

```bash
cd backend

# Run with auto-reload
uv run uvicorn app.main:app --reload

# Access API documentation
open http://localhost:8000/docs
```

### Frontend Development

```bash
cd frontend

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
Cbon/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── user/
│   │   │   ├── model.py
│   │   │   ├── schema.py
│   │   │   ├── routes.py
│   │   │   ├── auth_schema.py
│   │   │   └── auth_routes.py
│   │   ├── project/
│   │   │   ├── model.py
│   │   │   ├── schema.py
│   │   │   └── routes.py
│   │   ├── task/
│   │   │   ├── model.py
│   │   │   ├── schema.py
│   │   │   └── routes.py
│   │   ├── api_router.py
│   │   └── main.py
│   ├── docker-compose.yml
│   ├── pyproject.toml
│   └── schema.sql
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ProjectCard.vue
│   │   │   ├── ProjectList.vue
│   │   │   ├── ProjectModal.vue
│   │   │   ├── KanbanColumn.vue
│   │   │   ├── TaskModal.vue
│   │   │   └── TaskDetailModal.vue
│   │   ├── views/
│   │   │   ├── HomeView.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── RegisterView.vue
│   │   │   ├── ProjectsView.vue
│   │   │   └── ProjectDetailView.vue
│   │   ├── stores/
│   │   │   └── auth.ts
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   └── auth.ts
│   │   ├── router/
│   │   │   └── index.ts
│   │   └── App.vue
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## Security Notes

⚠️ **Important for Production:**

1. Change `SECRET_KEY` in `app/core/security.py`
2. Use environment variables for all secrets
3. Enable HTTPS
4. Configure proper CORS settings
5. Set up rate limiting
6. Use secure session management
7. Implement proper error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
