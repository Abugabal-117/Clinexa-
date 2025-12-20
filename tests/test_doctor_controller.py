"""
Unit tests for Doctor Controller
Tests doctor-related operations like schedule management and patient management
"""

import unittest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from controllers.doctor_controller import DoctorController
from models.doctor import Doctor
from core.authentication import Authentication
from repositories.repository_factory import RepositoryFactory


class TestDoctorController(unittest.TestCase):
    """Test cases for DoctorController class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_dir = tempfile.mkdtemp()
        os.environ['DATA_DIR'] = cls.test_dir
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures"""
        shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    def setUp(self):
        """Set up test data for each test"""
        self.doctor_id = "doctor_001"
        
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctor = Doctor(
            user_id=self.doctor_id,
            email="testdoctor@example.com",
            password_hash=Authentication.hash_password("TestPassword123"),
            first_name="Test",
            last_name="Doctor",
            specialization="General Practice"
        )
        doctor_repo.save(doctor)
    
    def test_add_available_time_success(self):
        """Test adding an available time slot for a doctor"""
        date = "2025-12-25"
        time = "10:00"
        
        result = DoctorController.add_available_time(
            self.doctor_id,
            date,
            time
        )
        
        self.assertTrue(result['success'])
        self.assertIn('message', result)
    
    def test_add_available_time_duplicate(self):
        """Test adding duplicate available time slot"""
        date = "2025-12-25"
        time = "10:00"
        
        result1 = DoctorController.add_available_time(
            self.doctor_id,
            date,
            time
        )
        self.assertTrue(result1['success'])
        
        result2 = DoctorController.add_available_time(
            self.doctor_id,
            date,
            time
        )
        self.assertFalse(result2['success'])
    
    def test_get_available_times(self):
        """Test retrieving available times for a doctor"""
        result = DoctorController.get_available_times(self.doctor_id)
        
        self.assertTrue(result['success'])
        self.assertIn('available_times', result)
        self.assertIsInstance(result['available_times'], list)
    
    def test_remove_available_time_success(self):
        """Test removing an available time slot"""
        date = "2025-12-26"
        time = "14:00"
        
        add_result = DoctorController.add_available_time(
            self.doctor_id,
            date,
            time
        )
        
        if add_result['success']:
            remove_result = DoctorController.remove_available_time(
                self.doctor_id,
                date,
                time
            )
            
            self.assertTrue(remove_result['success'])
    
    def test_remove_available_time_nonexistent(self):
        """Test removing a non-existent available time"""
        date = "2025-12-30"
        time = "16:00"
        
        result = DoctorController.remove_available_time(
            self.doctor_id,
            date,
            time
        )
        
        self.assertFalse(result['success'])
        self.assertIn('not found', result['message'])
    
    def test_get_doctor_success(self):
        """Test retrieving doctor information"""
        result = DoctorController.get_doctor(self.doctor_id)
        
        self.assertIn('success', result)
        if result['success']:
            self.assertIn('doctor', result)


if __name__ == '__main__':
    unittest.main()
