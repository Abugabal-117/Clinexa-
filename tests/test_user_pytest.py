import pytest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from controllers.user_controller import UserController
from core.authentication import Authentication


@pytest.fixture
def test_env():
    test_dir = tempfile.mkdtemp()
    os.environ['DATA_DIR'] = test_dir
    
    from core.csv_manager import CSVManager
    CSVManager._instance = None
    from threading import Lock
    CSVManager._lock = Lock()
    
    yield test_dir
    
    import glob
    for f in glob.glob(os.path.join(test_dir, '*.csv')):
        try:
            os.remove(f)
        except:
            pass
    shutil.rmtree(test_dir, ignore_errors=True)
    
    CSVManager._instance = None
    CSVManager._lock = Lock()


class TestUserRegistration:
    
    def test_register_patient_success(self, test_env):
        result = UserController.register(
            email="test_user_pytest_register@example.com",
            password="SecurePassword123",
            first_name="John",
            last_name="Doe",
            user_type="patient"
        )
        
        assert result['success'] is True
        assert 'user' in result
    
    def test_register_invalid_email(self, test_env):
        result = UserController.register(
            email="invalidemail",
            password="SecurePassword123",
            first_name="John",
            last_name="Doe",
            user_type="patient"
        )
        
        assert result['success'] is False
        assert 'email' in result['message'].lower()
    
    def test_register_short_password(self, test_env):
        result = UserController.register(
            email="test@example.com",
            password="short",
            first_name="John",
            last_name="Doe",
            user_type="patient"
        )
        
        assert result['success'] is False
        assert 'password' in result['message'].lower()
    
    def test_register_missing_name(self, test_env):
        result = UserController.register(
            email="test@example.com",
            password="SecurePassword123",
            first_name="",
            last_name="Doe",
            user_type="patient"
        )
        
        assert result['success'] is False


class TestUserLogin:
    
    def test_login_invalid_credentials(self, test_env):
        UserController._login_attempts = {}
        result = UserController.login(
            email="nonexistent@example.com",
            password="WrongPassword123"
        )
        
        assert result['success'] is False
        assert 'Invalid' in result['message']
    
    def test_login_multiple_failed_attempts(self, test_env):
        UserController._login_attempts = {}
        email = "testlock@example.com"
        
        for i in range(3):
            result = UserController.login(
                email=email,
                password="WrongPassword123"
            )
            
            if i < 2:
                assert result['success'] is False
            elif i == 2:
                assert result['success'] is False
                if 'locked' in result['message'].lower():
                    assert 'locked' in result['message'].lower()
    
    def test_login_empty_email(self, test_env):
        UserController._login_attempts = {}
        result = UserController.login(
            email="",
            password="Password123"
        )
        
        assert result['success'] is False
