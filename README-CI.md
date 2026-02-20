# CI/CD Pipeline Documentation

This project uses GitHub Actions for continuous integration and deployment.

## 🚀 CI Pipeline Features

- **Automated Testing**: Runs pytest on every push and pull request
- **Code Coverage**: Generates coverage reports with pytest-cov
- **Code Quality**: Linting with flake8 and formatting checks with black
- **Docker Build**: Builds and tests Docker image on successful test runs
- **Redis Service**: Automatically spins up Redis for integration tests

## 📋 Workflow Triggers

The CI pipeline runs on:
- Push to `main` or `develop` branches
- Pull requests to `main` branch

## 🔧 Setup Instructions

### 1. GitHub Secrets Configuration

Go to your repository → Settings → Secrets and Variables → Actions → New repository secret

Add the following secrets (optional - defaults provided for CI):

- `JWT_SECRET`: Secret key for JWT token generation
- `MONGO_URI`: MongoDB connection string
- `REDIS_HOST`: Redis host (defaults to localhost in CI)
- `SECRET_KEY`: Flask secret key

**Note**: The CI pipeline will use test defaults if secrets are not configured, but you should set them for production deployments.

### 2. Local Testing

To test the CI pipeline locally:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest --cov=app --cov-report=xml --cov-report=term

# Run linting
flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 app --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Check formatting
black --check app tests
```

### 3. Docker Build

Build the Docker image:

```bash
docker build -t website-extractor:latest .
```

Run the container:

```bash
docker run -p 5000:5000 \
  -e JWT_SECRET=your-secret \
  -e MONGO_URI=mongodb://localhost:27017/testdb \
  -e REDIS_HOST=localhost \
  -e REDIS_PORT=6379 \
  -e SECRET_KEY=your-secret-key \
  website-extractor:latest
```

## 📊 Coverage Reports

Coverage reports are generated in XML format and uploaded as artifacts. You can also integrate with Codecov for better visualization (optional).

## 🐳 Docker Image

The Dockerfile creates a production-ready image with:
- Python 3.12 slim base image
- Non-root user for security
- Health check endpoint
- Gunicorn WSGI server with 4 workers
- Optimized layer caching

## 🔍 Health Check

The application exposes a health check endpoint at `/api/health` that returns:
```json
{
  "status": "ok"
}
```

This is used by Docker's health check feature and can be used by orchestration tools like Kubernetes.

## 📝 Code Quality Standards

- **flake8**: Enforces PEP 8 style guide
- **black**: Ensures consistent code formatting
- **pytest**: Comprehensive test suite with coverage reporting

## 🚨 Troubleshooting

### Tests failing in CI but passing locally
- Ensure all dependencies are in `requirements.txt` or `requirements-dev.txt`
- Check that environment variables are properly set
- Verify Redis service is accessible

### Docker build failing
- Check Dockerfile syntax
- Ensure all files are included (check `.dockerignore`)
- Verify base image is accessible

### Coverage not uploading
- Check that `coverage.xml` is generated
- Verify artifact upload permissions
- Codecov integration is optional and won't fail the build
