from flask import render_template, redirect, url_for, session, flash, request
from controllers.patient_controller import PatientController
from controllers.doctor_controller import DoctorController
from controllers.auth_utils import login_required, patient_required
from utils.helpers import clean_str, get_booked_slots

def register_auth_routes(app):
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            from controllers.user_controller import UserController
            email = request.form.get('email')
            password = request.form.get('password')
            result = UserController.login(email, password)
            if result['success']:
                user = result['user']
                session['user'] = {
                    'id': user.user_id,
                    'name': user.get_full_name(),
                    'role': user.role,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
                return redirect(url_for('dashboard'))
            else:
                flash(result['message'], 'error')
        return render_template('login.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            from controllers.user_controller import UserController
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role', 'patient')
            result = UserController.register(email=email, password=password, first_name=first_name, last_name=last_name, user_type=role)
            if result['success']:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash(result['message'], 'error')
        return render_template('signup.html')

    @app.route('/logout')
    def logout():
        from controllers.user_controller import UserController
        session.clear()
        UserController.logout()
        return redirect(url_for('home'))

    @app.route('/forgot-password')
    def forgot_password():
        return render_template('forgot-password.html')

    @app.route('/reset-password')
    def reset_password():
        return render_template('reset-password.html')
