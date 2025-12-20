"""
Unit tests for Models
Tests data model creation, validation, and serialization
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from core.authentication import Authentication


class TestPatientModel(unittest.TestCase):
    """Test cases for Patient model"""
    
    def test_patient_creation(self):
        """Test creating a patient instance"""
        patient = Patient(
            user_id="p001",
            email="patient@example.com",
            password_hash=Authentication.hash_password("Password123"),
            first_name="John",
            last_name="Doe"
        )
        
        self.assertEqual(patient.user_id, "p001")
        self.assertEqual(patient.email, "patient@example.com")
        self.assertEqual(patient.first_name, "John")
        self.assertEqual(patient.last_name, "Doe")
    
    def test_patient_get_full_name(self):
        """Test getting patient's full name"""
        patient = Patient(
            user_id="p001",
            email="patient@example.com",
            password_hash=Authentication.hash_password("Password123"),
            first_name="John",
            last_name="Doe"
        )
        
        self.assertEqual(patient.get_full_name(), "John Doe")
    
    def test_patient_to_dict(self):
        """Test converting patient to dictionary"""
        patient = Patient(
            user_id="p001",
            email="patient@example.com",
            password_hash=Authentication.hash_password("Password123"),
            first_name="John",
            last_name="Doe"
        )
        
        patient_dict = patient.to_dict()
        
        self.assertEqual(patient_dict['user_id'], "p001")
        self.assertEqual(patient_dict['email'], "patient@example.com")
        self.assertEqual(patient_dict['first_name'], "John")


class TestDoctorModel(unittest.TestCase):
    """Test cases for Doctor model"""
    
    def test_doctor_creation(self):
        """Test creating a doctor instance"""
        doctor = Doctor(
            user_id="d001",
            email="doctor@example.com",
            password_hash=Authentication.hash_password("Password123"),
            first_name="Jane",
            last_name="Smith",
            specialization="Cardiology"
        )
        
        self.assertEqual(doctor.user_id, "d001")
        self.assertEqual(doctor.email, "doctor@example.com")
        self.assertEqual(doctor.specialization, "Cardiology")
        self.assertEqual(doctor.role, "doctor")
    
    def test_doctor_get_full_name(self):
        """Test getting doctor's full name"""
        doctor = Doctor(
            user_id="d001",
            email="doctor@example.com",
            password_hash=Authentication.hash_password("Password123"),
            first_name="Jane",
            last_name="Smith"
        )
        
        self.assertEqual(doctor.get_full_name(), "Jane Smith")
    
    def test_doctor_add_patient(self):
        """Test adding a patient to doctor's patient list"""
        doctor = Doctor(
            user_id="d001",
            email="doctor@example.com",
            password_hash=Authentication.hash_password("Password123"),
            first_name="Jane",
            last_name="Smith"
        )
        
        doctor.add_patient("p001")
        
        self.assertIn("p001", doctor.patients)
    
    def test_doctor_to_dict(self):
        """Test converting doctor to dictionary"""
        doctor = Doctor(
            user_id="d001",
            email="doctor@example.com",
            password_hash=Authentication.hash_password("Password123"),
            first_name="Jane",
            last_name="Smith",
            specialization="Neurology",
            license_number="LIC123"
        )
        
        doctor_dict = doctor.to_dict()
        
        self.assertEqual(doctor_dict['user_id'], "d001")
        self.assertEqual(doctor_dict['specialization'], "Neurology")
        self.assertEqual(doctor_dict['license_number'], "LIC123")


class TestAppointmentModel(unittest.TestCase):
    """Test cases for Appointment model"""
    
    def test_appointment_creation(self):
        """Test creating an appointment instance"""
        appointment = Appointment(
            appointment_id="apt001",
            patient_id="p001",
            doctor_id="d001",
            appointment_date="2025-12-25",
            appointment_time="10:00",
            status="confirmed"
        )
        
        self.assertEqual(appointment.appointment_id, "apt001")
        self.assertEqual(appointment.patient_id, "p001")
        self.assertEqual(appointment.doctor_id, "d001")
        self.assertEqual(appointment.appointment_date, "2025-12-25")
        self.assertEqual(appointment.appointment_time, "10:00")
        self.assertEqual(appointment.status, "confirmed")
    
    def test_appointment_to_dict(self):
        """Test converting appointment to dictionary"""
        appointment = Appointment(
            appointment_id="apt001",
            patient_id="p001",
            doctor_id="d001",
            appointment_date="2025-12-25",
            appointment_time="10:00",
            status="confirmed",
            reason="Checkup"
        )
        
        apt_dict = appointment.to_dict()
        
        self.assertEqual(apt_dict['appointment_id'], "apt001")
        self.assertEqual(apt_dict['status'], "confirmed")
        self.assertEqual(apt_dict['reason'], "Checkup")


if __name__ == '__main__':
    unittest.main()
