import pytest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from app import app
from core.authentication import Authentication


@pytest.fixture(scope="class")
def test_env():
    test_dir = tempfile.mkdtemp()
    os.environ['DATA_DIR'] = test_dir
    app.config['TESTING'] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    yield
    shutil.rmtree(test_dir, ignore_errors=True)


@pytest.fixture
def client(test_env):
    return app.test_client()


class TestAppRoutes:
    
    def test_home_page_loads(self, client):
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'Welcome to Your Healthcare Portal' in response.data
    
    def test_login_page_loads(self, client):
        response = client.get('/login')
        
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_signup_page_loads(self, client):
        response = client.get('/signup')
        
        assert response.status_code == 200
        assert b'Create Account' in response.data
    
    def test_login_post_invalid_credentials(self, client):
        response = client.post('/login', data={
            'email': 'nonexistent@example.com',
            'password': 'WrongPassword123'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_logout_route(self, client):
        response = client.get('/logout')
        
        assert response.status_code in [200, 302]
    
    def test_forgot_password_page_loads(self, client):
        response = client.get('/forgot-password')
        
        assert response.status_code == 200
    
    def test_reset_password_page_loads(self, client):
        response = client.get('/reset-password')
        
        assert response.status_code == 200
    
    def test_about_doctor_page_loads(self, client):
        response = client.get('/about-doctor')
        
        assert response.status_code == 200
    
    def test_unauthenticated_dashboard_redirect(self, client):
        response = client.get('/dashboard')
        
        assert response.status_code in [302, 303, 307, 308]


class TestPasswordSecurity:
    
    def test_password_not_stored_plain_text(self):
        password = "MySecurePassword123"
        password_hash = Authentication.hash_password(password)
        
        assert password != password_hash
    
    def test_password_hash_is_deterministic(self):
        password = "TestPassword123"
        
        hash1 = Authentication.hash_password(password)
        hash2 = Authentication.hash_password(password)
        
        assert hash1 == hash2
    
    def test_password_verification_works(self):
        password = "TestPassword123"
        wrong_password = "WrongPassword456"
        
        password_hash = Authentication.hash_password(password)
        
        assert Authentication.verify_password(password, password_hash) is True
        assert Authentication.verify_password(wrong_password, password_hash) is False
