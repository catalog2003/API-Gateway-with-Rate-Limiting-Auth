# 🚀 API Gateway with Rate Limiting & Authentication

A production-ready API Gateway built with Flask that provides authentication, rate limiting, and web content extraction capabilities. This project demonstrates modern Python backend development practices with comprehensive testing, CI/CD pipelines, and Docker containerization.

## ✨ Features

- **🔐 JWT Authentication** - Secure user registration and login with JWT tokens
- **⚡ Rate Limiting** - Token bucket algorithm implemented with Redis for scalable rate limiting
- **🌐 Web Content Extraction** - Extract text and metadata from web pages using BeautifulSoup
- **📊 Role-Based Access Control** - Different rate limits for free and paid users
- **🏥 Health Checks** - Health monitoring endpoint for orchestration tools
- **📈 Metrics & Monitoring** - Prometheus metrics integration
- **🐳 Docker Support** - Production-ready Docker containerization
- **🔄 CI/CD Pipeline** - Automated testing and deployment with GitHub Actions
- **✅ Comprehensive Testing** - Unit and integration tests with pytest

## 🛠️ Tech Stack

- **Framework**: Flask (Python 3.12)
- **Database**: MongoDB (via pymongo)
- **Cache/Rate Limiting**: Redis
- **Authentication**: JWT (PyJWT) + bcrypt
- **Web Scraping**: BeautifulSoup4
- **Validation**: Pydantic
- **Testing**: pytest, pytest-cov, pytest-mock
- **Code Quality**: flake8, black
- **WSGI Server**: Gunicorn
- **Containerization**: Docker

## 📋 Prerequisites

- Python 3.12+
- MongoDB (running locally or connection string)
- Redis (running locally or connection string)
- Git

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/catalog2003/API-Gateway-with-Rate-Limiting-Auth.git
cd API-Gateway-with-Rate-Limiting-Auth
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
MONGO_URI=mongodb://localhost:27017/text_extract
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 5. Start Services

Make sure MongoDB and Redis are running:

```bash
# MongoDB (if running locally)
mongod

# Redis (if running locally)
redis-server
```

### 6. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## 📡 API Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "role": "free"  // or "paid"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user_id": "507f1f77bcf86cd799439011"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer"
}
```

### Protected Endpoints

All protected endpoints require authentication via Bearer token:

```http
Authorization: Bearer <your-access-token>
```

#### Extract Web Content
```http
POST /api/extract
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "title": "Example Domain",
  "text": "This domain is for use in illustrative examples...",
  "word_count": 25,
  "extraction_id": "507f1f77bcf86cd799439012"
}
```

#### Get User Profile
```http
GET /api/profile
Authorization: Bearer <token>
```

**Response:**
```json
{
  "email": "user@example.com",
  "role": "free"
}
```

### Health Check

```http
GET /api/health
```

**Response:**
```json
{
  "status": "ok"
}
```

## 🔒 Rate Limiting

The API implements a token bucket rate limiting algorithm:

- **Free Users**: 5 requests per minute
- **Paid Users**: 10 requests per minute

Rate limit information is included in response headers:

```
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 4
```

When rate limit is exceeded, the API returns:

```json
{
  "error": "Rate limit exceeded"
}
```

Status Code: `429 Too Many Requests`

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=term --cov-report=xml
```

### Run Specific Test Files

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/
```

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t api-gateway:latest .
```

### Run Docker Container

```bash
docker run -d -p 5000:5000 \
  -e JWT_SECRET=your-jwt-secret \
  -e MONGO_URI=mongodb://host.docker.internal:27017/text_extract \
  -e REDIS_HOST=host.docker.internal \
  -e REDIS_PORT=6379 \
  -e SECRET_KEY=your-secret-key \
  --name api-gateway \
  api-gateway:latest
```

### Docker Compose (Example)

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - JWT_SECRET=${JWT_SECRET}
      - MONGO_URI=mongodb://mongo:27017/text_extract
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - mongo
      - redis
  
  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

## 🔄 CI/CD Pipeline

This project includes a comprehensive GitHub Actions CI/CD pipeline that:

- ✅ Runs automated tests on every push/PR
- ✅ Generates code coverage reports
- ✅ Performs code quality checks (flake8, black)
- ✅ Builds and tests Docker images
- ✅ Uploads coverage artifacts

View the pipeline status in the [Actions](https://github.com/catalog2003/API-Gateway-with-Rate-Limiting-Auth/actions) tab.

### Configure GitHub Secrets

For production deployments, configure these secrets in GitHub:

- `JWT_SECRET`
- `MONGO_URI`
- `REDIS_HOST`
- `SECRET_KEY`

Go to: Repository → Settings → Secrets and Variables → Actions

## 📁 Project Structure

```
api-gateway/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration
│   ├── core/                # Core utilities
│   │   ├── logger.py
│   │   └── security.py
│   ├── extensions/          # Flask extensions
│   │   ├── jwt_handler.py
│   │   ├── mongo.py
│   │   ├── redis_client.py
│   │   └── metrics.py
│   ├── middleware/          # Custom middleware
│   │   ├── auth_middleware.py
│   │   └── rate_limiter.py
│   ├── models/              # Data models
│   │   ├── user_model.py
│   │   └── extraction_model.py
│   ├── repositories/        # Data access layer
│   │   ├── user_repository.py
│   │   └── extraction_repository.py
│   ├── routes/              # API routes
│   │   ├── auth_routes.py
│   │   ├── extraction_routes.py
│   │   ├── protected_routes.py
│   │   └── health_routes.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── auth_schema.py
│   │   └── extraction_schema.py
│   └── services/            # Business logic
│       ├── auth_service.py
│       ├── extraction_service.py
│       └── rate_limiter_service.py
├── tests/
│   ├── conftest.py          # Pytest configuration
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions workflow
├── Dockerfile               # Docker configuration
├── .dockerignore
├── .gitignore
├── requirements.txt         # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── pytest.ini              # Pytest configuration
├── run.py                  # Application entry point
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | Required |
| `JWT_SECRET` | JWT signing secret | Required |
| `MONGO_URI` | MongoDB connection string | Required |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |

### Rate Limiting Configuration

Rate limits are configured in `app/services/rate_limiter_service.py`:

```python
ROLE_LIMITS = {
    "free": {"capacity": 5, "refill_rate": 5/60},   # 5 requests per minute
    "paid": {"capacity": 10, "refill_rate": 10/60}   # 10 requests per minute
}
```

## 📊 Monitoring

### Health Check

Monitor application health:

```bash
curl http://localhost:5000/api/health
```

### Metrics

Prometheus metrics are available at `/metrics` endpoint (if configured).

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**catalog2003**

- GitHub: [@catalog2003](https://github.com/catalog2003)

## 🙏 Acknowledgments

- Flask community for the excellent framework
- Redis for scalable caching solutions
- MongoDB for flexible document storage
- All contributors and open-source libraries used in this project

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Redis Documentation](https://redis.io/docs/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Docker Documentation](https://docs.docker.com/)

---

⭐ If you find this project useful, please consider giving it a star!
