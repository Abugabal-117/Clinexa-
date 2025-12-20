"""
Integration tests for the Clinic System
Tests interactions between multiple components and Flask routes
"""

import unittest
import sys
import os
import tempfile
import shutil
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from app import app
from core.authentication import Authentication


class TestAppRoutes(unittest.TestCase):
    """Test cases for Flask application routes"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_dir = tempfile.mkdtemp()
        os.environ['DATA_DIR'] = cls.test_dir
        
        app.config['TESTING'] = True
        app.config['SESSION_TYPE'] = 'filesystem'
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures"""
        shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    def setUp(self):
        """Create test client for each test"""
        self.client = app.test_client()
    
    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Your Healthcare Portal', response.data)
    
    def test_login_page_loads(self):
        """Test that login page loads successfully"""
        response = self.client.get('/login')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_signup_page_loads(self):
        """Test that signup page loads successfully"""
        response = self.client.get('/signup')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Account', response.data)
    
    def test_login_post_invalid_credentials(self):
        """Test login POST with invalid credentials"""
        response = self.client.post('/login', data={
            'email': 'nonexistent@example.com',
            'password': 'WrongPassword123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_logout_route(self):
        """Test logout route"""
        response = self.client.get('/logout')
        
        self.assertIn(response.status_code, [200, 302])
    
    def test_forgot_password_page_loads(self):
        """Test that forgot password page loads"""
        response = self.client.get('/forgot-password')
        
        self.assertEqual(response.status_code, 200)
    
    def test_reset_password_page_loads(self):
        """Test that reset password page loads"""
        response = self.client.get('/reset-password')
        
        self.assertEqual(response.status_code, 200)
    
    def test_about_doctor_page_loads(self):
        """Test that about doctor page loads"""
        response = self.client.get('/about-doctor')
        
        self.assertEqual(response.status_code, 200)
    
    def test_unauthenticated_dashboard_redirect(self):
        """Test that unauthenticated users are redirected from dashboard"""
        response = self.client.get('/dashboard')
        
        self.assertIn(response.status_code, [302, 303, 307, 308])


class TestPasswordSecurity(unittest.TestCase):
    """Test cases for password security"""
    
    def test_password_not_stored_plain_text(self):
        """Test that passwords are not stored in plain text"""
        password = "MySecurePassword123"
        password_hash = Authentication.hash_password(password)
        
        self.assertNotEqual(password, password_hash)
    
    def test_password_hash_is_deterministic(self):
        """Test that password hashing is deterministic"""
        password = "TestPassword123"
        
        hash1 = Authentication.hash_password(password)
        hash2 = Authentication.hash_password(password)
        
        self.assertEqual(hash1, hash2)
    
    def test_password_verification_works(self):
        """Test that password verification works correctly"""
        password = "TestPassword123"
        wrong_password = "WrongPassword456"
        
        password_hash = Authentication.hash_password(password)
        
        self.assertTrue(Authentication.verify_password(password, password_hash))
        
        self.assertFalse(Authentication.verify_password(wrong_password, password_hash))


if __name__ == '__main__':
    unittest.main()
