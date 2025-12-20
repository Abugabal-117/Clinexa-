from flask import render_template, redirect, url_for, session, request
from controllers.doctor_controller import DoctorController
from controllers.user_controller import UserController
from controllers.auth_utils import refresh_session_user, login_required

def register_profile_routes(app):
    
    @app.route('/doctor-profile', defaults={'doctor_id': None})
    @app.route('/doctor-profile/<doctor_id>')
    @login_required
    def doctor_profile(doctor_id):
        if not doctor_id:
            if session.get('user', {}).get('role') == 'doctor':
                doctor_id = session['user']['id']
            else:
                docs = DoctorController.get_all_doctors()['doctors']
                doctor_id = docs[0].user_id if docs else None
        if not doctor_id:
            return redirect(url_for('dashboard'))
        doc_res = DoctorController.get_doctor(doctor_id)
        if doc_res['success']:
            feedback = DoctorController.get_feedback(doctor_id).get('feedback', [])
            return render_template('doctor-profile.html', doctor=doc_res['doctor'], feedback=feedback)
        return redirect(url_for('dashboard'))

    @app.route('/edit-profile', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        if request.method == 'POST':
            updates = {k: v for k, v in request.form.items() if v}
            UserController.update_profile(session['user']['id'], session['user']['id'], **updates)
            refresh_session_user(session['user']['id'])
            return redirect(url_for('edit_profile'))
        user = UserController.get_profile(session['user']['id'])['user']
        return render_template('edit-profile.html', user=user)

    @app.route('/about-doctor')
    def about_doctor():
        doctors_result = DoctorController.get_all_doctors()
        doctors = doctors_result.get('doctors', []) if doctors_result['success'] else []
        doctor = doctors[0] if doctors else None
        return render_template('about-doctor.html', doctor=doctor)
