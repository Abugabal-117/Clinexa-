from flask import render_template, redirect, url_for, session
from controllers.patient_controller import PatientController
from controllers.doctor_controller import DoctorController
from controllers.auth_utils import login_required, patient_required

def register_core_routes(app):
    
    @app.route('/')
    def home():
        if 'user' in session:
            return redirect(url_for('dashboard'))
        return render_template('index.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        user = session['user']
        role = user.get('role', 'patient')
        if role == 'patient':
            appointments_result = PatientController.get_appointments(user['id'])
            appointments = appointments_result['appointments'] if appointments_result['success'] else []
            return render_template('dashboard.html', user=user, appointments=appointments)
        elif role == 'doctor':
            return render_template('doctor-dashboard.html', user=user)
        return render_template('dashboard.html', user=user, appointments=[])

    @app.route('/doctor-login')
    def doctor_login():
        return render_template('doctor-login.html')

    @app.route('/rating', methods=['GET', 'POST'])
    @patient_required
    def rating():
        return redirect(url_for('dashboard'))
