"""
Unit tests for Patient Controller
Tests patient creation, retrieval, and patient-related operations
"""

import unittest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from controllers.patient_controller import PatientController
from models.patient import Patient
from core.authentication import Authentication


class TestPatientController(unittest.TestCase):
    """Test cases for PatientController class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for the entire test class"""
        cls.test_dir = tempfile.mkdtemp()
        os.environ['DATA_DIR'] = cls.test_dir
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures"""
        shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    def setUp(self):
        """Clear data before each test"""
        import glob
        data_files = glob.glob(os.path.join(self.test_dir, '*.json'))
        for f in data_files:
            try:
                os.remove(f)
            except:
                pass
    
    def test_create_patient_success(self):
        """Test successful patient creation"""
        email = "test_create_patient_success@example.com"
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
        
        self.assertTrue(result['success'])
        self.assertIn('patient', result)
        self.assertEqual(result['patient'].email, email)
        self.assertEqual(result['patient'].first_name, first_name)
    
    def test_create_patient_duplicate_email(self):
        """Test patient creation with duplicate email"""
        email = "test_duplicate@example.com"
        password_hash = Authentication.hash_password("Password123")
        
        result1 = PatientController.create_patient(
            email=email,
            password_hash=password_hash,
            first_name="First",
            last_name="Patient"
        )
        self.assertTrue(result1['success'])
        
        result2 = PatientController.create_patient(
            email=email,
            password_hash=password_hash,
            first_name="Second",
            last_name="Patient"
        )
        self.assertFalse(result2['success'])
        self.assertIn('already exists', result2['message'])
    
    def test_get_all_patients(self):
        """Test retrieving all patients"""
        result = PatientController.get_all_patients()
        
        self.assertTrue(result['success'])
        self.assertIn('patients', result)
        self.assertIsInstance(result['patients'], list)
    
    def test_update_patient_success(self):
        """Test successful patient update"""
        email = "test_update@example.com"
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
            
            self.assertTrue(update_result['success'])
            self.assertEqual(update_result['patient'].first_name, "New")
    
    def test_get_appointments_empty(self):
        """Test getting appointments for a patient with no appointments"""
        email = "test_appointments@example.com"
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
            
            self.assertTrue(appt_result['success'])
            self.assertIsInstance(appt_result['appointments'], list)


if __name__ == '__main__':
    unittest.main()
