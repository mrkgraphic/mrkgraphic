# BusinessHub - Business Profile SaaS Platform

A comprehensive SaaS platform for creating and managing business profiles. Built with FastAPI (Python) backend and React (TypeScript) frontend.

## 🚀 Features

### Core Features
- **Business Profile Management**: Create, edit, and manage comprehensive business profiles
- **User Authentication**: Secure JWT-based authentication system
- **File Upload**: Image upload for logos and business photos with compression
- **Review System**: Customer reviews and ratings
- **Business Directory**: Public directory of published business profiles
- **Search & Filter**: Advanced search and filtering capabilities
- **SEO Optimization**: Meta tags and SEO-friendly URLs

### Technical Features
- **REST API**: Comprehensive FastAPI backend with OpenAPI documentation
- **Async Database**: SQLAlchemy with async PostgreSQL support
- **Modern Frontend**: React 18 with TypeScript and Tailwind CSS
- **Real-time UI**: Toast notifications and responsive design
- **Form Validation**: Zod schema validation with React Hook Form
- **State Management**: React Context API for authentication and global state

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM with async support
- **PostgreSQL** - Primary database
- **JWT** - Authentication tokens
- **Pydantic** - Data validation
- **Alembic** - Database migrations
- **Python 3.9+**

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **React Hook Form** - Form handling
- **Zod** - Schema validation
- **Axios** - HTTP client
- **Lucide React** - Icons

## 📦 Project Structure

```
business-profile-saas/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core functionality (auth, config)
│   │   ├── db/             # Database configuration
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── utils/          # Utility functions
│   ├── main.py             # FastAPI app entry point
│   └── requirements.txt    # Python dependencies
├── src/                    # React frontend
│   ├── components/         # React components
│   ├── contexts/           # React contexts
│   ├── pages/              # Page components
│   ├── services/           # API services
│   └── App.tsx             # Main app component
├── package.json            # Node.js dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd business-profile-saas
   ```

2. **Set up Python virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```bash
   # Create database
   createdb business_saas
   ```

5. **Configure environment variables**
   ```bash
   # Create .env file in backend directory
   cat > .env << EOF
   DATABASE_URL=postgresql://username:password@localhost/business_saas
   SECRET_KEY=your-secret-key-change-this-in-production
   SMTP_HOST=your-smtp-host
   SMTP_USER=your-smtp-user
   SMTP_PASSWORD=your-smtp-password
   STRIPE_SECRET_KEY=your-stripe-secret-key
   STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
   EOF
   ```

6. **Run database migrations**
   ```bash
   # The app will create tables automatically on startup
   # For production, use Alembic migrations
   ```

7. **Start the backend server**
   ```bash
   cd backend
   python main.py
   # Or use uvicorn directly:
   # uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Install Node.js dependencies**
   ```bash
   npm install
   ```

2. **Configure environment variables**
   ```bash
   # Create .env file in root directory
   cat > .env << EOF
   VITE_API_URL=http://localhost:8000/api/v1
   EOF
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## 🐳 Docker Setup (Optional)

### Using Docker Compose

1. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   services:
     postgres:
       image: postgres:13
       environment:
         POSTGRES_DB: business_saas
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD: password
       ports:
         - "5432:5432"
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
     backend:
       build: ./backend
       ports:
         - "8000:8000"
       environment:
         DATABASE_URL: postgresql://postgres:password@postgres/business_saas
       depends_on:
         - postgres
   
     frontend:
       build: .
       ports:
         - "3000:3000"
       environment:
         VITE_API_URL: http://localhost:8000/api/v1
       depends_on:
         - backend
   
   volumes:
     postgres_data:
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

### Business Profile Endpoints
- `GET /api/v1/business-profiles/` - Get user's profiles
- `POST /api/v1/business-profiles/` - Create new profile
- `GET /api/v1/business-profiles/{id}` - Get specific profile
- `PUT /api/v1/business-profiles/{id}` - Update profile
- `DELETE /api/v1/business-profiles/{id}` - Delete profile
- `GET /api/v1/business-profiles/public` - Get public profiles
- `GET /api/v1/business-profiles/public/{slug}` - Get public profile by slug

### File Upload Endpoints
- `POST /api/v1/business-profiles/{id}/upload-logo` - Upload business logo

### Review Endpoints
- `POST /api/v1/business-profiles/{id}/reviews` - Create review
- `GET /api/v1/business-profiles/{id}/reviews` - Get profile reviews

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
npm run test
```

## 🚀 Deployment

### Backend Deployment (Railway/Heroku)

1. **Set up environment variables**
2. **Deploy with git push**
3. **Run database migrations**

### Frontend Deployment (Vercel/Netlify)

1. **Build the project**
   ```bash
   npm run build
   ```

2. **Deploy the `dist` folder**

### Database Deployment

1. **Use managed PostgreSQL** (AWS RDS, Railway, etc.)
2. **Update `DATABASE_URL` environment variable**

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@localhost/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
MAX_FILE_SIZE=10485760
UPLOAD_FOLDER=static/uploads
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
```

#### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 📖 Development Guide

### Adding New Features

1. **Backend**: Add models, schemas, and API endpoints
2. **Frontend**: Create components and integrate with API
3. **Database**: Create migrations for schema changes

### Code Style

- **Backend**: Follow PEP 8, use Black formatter
- **Frontend**: Use ESLint and Prettier
- **Git**: Conventional commits

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migration
alembic upgrade head
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `/docs` endpoint for API documentation
- **Issues**: Create an issue on GitHub
- **Email**: Support contact information

## 🎯 Roadmap

- [ ] Payment integration with Stripe
- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Multi-language support
- [ ] API rate limiting
- [ ] Advanced search with Elasticsearch
- [ ] Real-time chat support

---

**Made with ❤️ by the BusinessHub Team**
