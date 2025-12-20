import pytest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from controllers.patient_controller import PatientController
from models.patient import Patient
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


class TestPatientController:
    
    def test_create_patient_success(self, test_env):
        email = "test_pytest_create_success@example.com"
        password = "TestPassword123"
        first_name = "John"
        last_name = "Doe"
        
        password_hash = Authentication.hash_password(password)
        result = PatientController.create_patient(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name
        )
        
        assert result['success'] is True
        assert 'patient' in result
        assert result['patient'].email == email
        assert result['patient'].first_name == first_name
    
    def test_create_patient_duplicate_email(self, test_env):
        email = "test_pytest_duplicate@example.com"
        password_hash = Authentication.hash_password("Password123")
        
        result1 = PatientController.create_patient(
            email=email,
            password_hash=password_hash,
            first_name="First",
            last_name="Patient"
        )
        assert result1['success'] is True
        
        result2 = PatientController.create_patient(
            email=email,
            password_hash=password_hash,
            first_name="Second",
            last_name="Patient"
        )
        assert result2['success'] is False
        assert 'already exists' in result2['message']
    
    def test_get_all_patients(self, test_env):
        result = PatientController.get_all_patients()
        
        assert result['success'] is True
        assert 'patients' in result
        assert isinstance(result['patients'], list)
    
    def test_update_patient_success(self, test_env):
        email = "test_pytest_update@example.com"
        password_hash = Authentication.hash_password("Password123")
        
        result = PatientController.create_patient(
            email=email,
            password_hash=password_hash,
            first_name="Old",
            last_name="Name"
        )
        
        if result['success']:
            patient_id = result['patient'].user_id
            
            update_result = PatientController.update_patient(
                patient_id=patient_id,
                first_name="New",
                last_name="Name"
            )
            
            assert update_result['success'] is True
            assert update_result['patient'].first_name == "New"
    
    def test_get_appointments_empty(self, test_env):
        email = "test_pytest_appointments@example.com"
        password_hash = Authentication.hash_password("Password123")
        
        result = PatientController.create_patient(
            email=email,
            password_hash=password_hash,
            first_name="Test",
            last_name="Patient"
        )
        
        if result['success']:
            patient_id = result['patient'].user_id
            
            appt_result = PatientController.get_appointments(patient_id)
            
            assert appt_result['success'] is True
            assert isinstance(appt_result['appointments'], list)
