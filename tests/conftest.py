import sys
import os
import pytest
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.fixture(autouse=True)
def reset_csv_manager():
    """Reset CSVManager singleton before each test"""
    from core.csv_manager import CSVManager
    CSVManager._instance = None
    CSVManager._lock = __import__('threading').Lock()
    yield
    CSVManager._instance = None
    CSVManager._lock = __import__('threading').Lock()

@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary test data directory"""
    return str(tmp_path)

@pytest.fixture
def app(test_data_dir, monkeypatch):
    monkeypatch.setenv('TESTING', 'True')
    monkeypatch.setenv('DATA_DIR', test_data_dir)
    
    from core.csv_manager import CSVManager
    CSVManager._instance = None
    CSVManager._lock = __import__('threading').Lock()
    
    from app import app as flask_app
    
    flask_app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key-with-sufficient-length-for-security',
        'WTF_CSRF_ENABLED': False
    })
    
    yield flask_app
    
    CSVManager._instance = None
    CSVManager._lock = __import__('threading').Lock()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
