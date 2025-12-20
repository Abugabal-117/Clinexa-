from flask import render_template, redirect, url_for, session, flash, request
from controllers.doctor_controller import DoctorController
from controllers.auth_utils import login_required

def register_doctor_routes(app):
    
    @app.route('/schedule-management', methods=['GET', 'POST'])
    @login_required
    def schedule_management():
        if session['user']['role'] != 'doctor':
            return redirect(url_for('dashboard'))
        doctor_id = session['user']['id']
        if request.method == 'POST':
            action = request.form.get('action')
            day = request.form.get('day')
            time = request.form.get('time')
            if action == 'add':
                DoctorController.add_available_time(doctor_id, day, time)
                flash('Slot added', 'success')
            elif action == 'remove':
                DoctorController.remove_available_time(doctor_id, day, time)
                flash('Slot removed', 'success')
            return redirect(url_for('schedule_management'))
        result = DoctorController.get_available_times(doctor_id)
        return render_template('schedule-management.html', available_times=result.get('available_times', []))

    @app.route('/patient-report', methods=['GET', 'POST'])
    @login_required
    def patient_report():
        if session['user']['role'] != 'doctor':
            return redirect(url_for('dashboard'))
        doctor_id = session['user']['id']
        if request.method == 'POST':
            DoctorController.create_report(doctor_id, request.form.get('patient_id'), request.form.get('patient_name_hidden'), request.form.get('report_details'))
            return redirect(url_for('patient_report'))
        patients = DoctorController.get_all_patients()
        reports = DoctorController.get_doctor_reports(doctor_id).get('reports', [])
        return render_template('patient-report.html', patients=patients, reports=reports)

    @app.route('/remove-patient/<patient_id>', methods=['POST'])
    @login_required
    def remove_patient(patient_id):
        DoctorController.remove_patient(session['user']['id'], patient_id)
        return redirect(url_for('appointments'))
