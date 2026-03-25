import os
import sys
import json

# provide minimal env defaults so create_app() can run in this test script
os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PORT", "6379")
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017/testdb")
os.environ.setdefault("SECRET_KEY", "dev")
os.environ.setdefault("JWT_SECRET", "dev")

# ensure project root (api-gateway) is on sys.path when running as a script
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app

app = create_app()

# Test via HTTP endpoint
with app.test_client() as client:
    # First, login to get a token
    response = client.post('/api/auth/register', 
        json={'email': 'test@example.com', 'password': 'testpass'},
        content_type='application/json')
    print(f"Register response: {response.status_code}")
    
    response = client.post('/api/auth/login',
        json={'email': 'test@example.com', 'password': 'testpass'},
        content_type='application/json')
    data = response.get_json()
    print(f"Login response: {response.status_code}, Body: {data}")
    token = data.get('token') or data.get('access_token')
    print(f"Token: {token}")
    
    # Now test rate limiting on protected endpoint
    headers = {'Authorization': f'Bearer {token}'}
    for i in range(7):
        response = client.get('/api/profile', headers=headers)
        print(f"Request {i+1}: {response.status_code} - Remaining: {response.headers.get('X-RateLimit-Remaining')}")
        if response.status_code == 429:
            print(f"  Error: {response.get_json()}")




