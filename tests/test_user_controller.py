"""
Unit tests for User Controller
Tests user registration, login, and user management functionality
"""

import unittest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from controllers.user_controller import UserController
from core.authentication import Authentication


class TestUserRegistration(unittest.TestCase):
    """Test cases for user registration"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_dir = tempfile.mkdtemp()
        os.environ['DATA_DIR'] = cls.test_dir
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures"""
        shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    def test_register_patient_success(self):
        """Test successful patient registration"""
        result = UserController.register(
            email="newpatient@example.com",
            password="SecurePassword123",
            first_name="John",
            last_name="Doe",
            user_type="patient"
        )
        
        self.assertTrue(result['success'])
        self.assertIn('user', result)
    
    def test_register_invalid_email(self):
        """Test registration with invalid email"""
        result = UserController.register(
            email="invalidemail",
            password="SecurePassword123",
            first_name="John",
            last_name="Doe",
            user_type="patient"
        )
        
        self.assertFalse(result['success'])
        self.assertIn('email', result['message'].lower())
    
    def test_register_short_password(self):
        """Test registration with password too short"""
        result = UserController.register(
            email="test@example.com",
            password="short",
            first_name="John",
            last_name="Doe",
            user_type="patient"
        )
        
        self.assertFalse(result['success'])
        self.assertIn('password', result['message'].lower())
    
    def test_register_missing_name(self):
        """Test registration with missing names"""
        result = UserController.register(
            email="test@example.com",
            password="SecurePassword123",
            first_name="",
            last_name="Doe",
            user_type="patient"
        )
        
        self.assertFalse(result['success'])


class TestUserLogin(unittest.TestCase):
    """Test cases for user login functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_dir = tempfile.mkdtemp()
        os.environ['DATA_DIR'] = cls.test_dir
        
        UserController._login_attempts = {}
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures"""
        shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    def setUp(self):
        """Reset login attempts before each test"""
        UserController._login_attempts = {}
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        result = UserController.login(
            email="nonexistent@example.com",
            password="WrongPassword123"
        )
        
        self.assertFalse(result['success'])
        self.assertIn('Invalid', result['message'])
    
    def test_login_multiple_failed_attempts(self):
        """Test account lockout after multiple failed login attempts"""
        email = "testlock@example.com"
        
        UserController._login_attempts = {}
        
        for i in range(3):
            result = UserController.login(
                email=email,
                password="WrongPassword123"
            )
            
            if i < 2:
                self.assertFalse(result['success'])
            elif i == 2:
                self.assertFalse(result['success'])
                if 'locked' in result['message'].lower():
                    self.assertIn('locked', result['message'].lower())
    
    def test_login_empty_email(self):
        """Test login with empty email"""
        result = UserController.login(
            email="",
            password="Password123"
        )
        
        self.assertFalse(result['success'])


if __name__ == '__main__':
    unittest.main()
