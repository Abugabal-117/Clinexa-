from flask import render_template, redirect, url_for, session, flash, request
from controllers.patient_controller import PatientController
from controllers.doctor_controller import DoctorController
from controllers.auth_utils import login_required, patient_required
from utils.helpers import clean_str, get_booked_slots

def register_patient_routes(app):
    
    @app.route('/booking', methods=['GET', 'POST'])
    @patient_required
    def booking():
        doctors_result = DoctorController.get_all_doctors()
        doctors = doctors_result.get('doctors', []) if doctors_result['success'] else []
        
        if not doctors:
            flash('No doctors available', 'error')
            return redirect(url_for('dashboard'))
        
        selected_doctor = doctors[0]
        doctor_id = selected_doctor.user_id
        
        if request.method == 'POST':
            selection = request.form.get('slot_selection')
            reason = request.form.get('reason')
            
            if selection:
                day_part, time_part = selection.split('|')
                day_part = clean_str(day_part)
                time_part = clean_str(time_part)
                
                taken_times = get_booked_slots(doctor_id, day_part)
                
                if time_part in taken_times:
                    flash('Error: This slot was just booked by someone else!', 'error')
                else:
                    result = PatientController.book_appointment(
                        patient_id=session['user']['id'],
                        doctor_id=doctor_id,
                        appointment_date=day_part,
                        appointment_time=time_part,
                        reason=reason
                    )
                    if result['success']:
                        flash('Appointment booked successfully!', 'success')
                        DoctorController.remove_available_time(doctor_id, day_part, time_part)
                        return redirect(url_for('booking')) 
                    else:
                        flash(result.get('message', 'Booking failed'), 'error')
            else:
                flash('Please select a time slot.', 'error')
            
            return redirect(url_for('booking'))

        all_slots_result = DoctorController.get_available_times(doctor_id)
        all_slots = all_slots_result.get('available_times', []) if all_slots_result['success'] else []

        weekly_schedule = {}
        
        print("\n=== START FILTERING ===")
        
        slots_by_day = {}
        for slot in all_slots:
            d = clean_str(slot['date'])
            t = clean_str(slot['time'])
            if d not in slots_by_day: slots_by_day[d] = []
            slots_by_day[d].append(t)
            
        for day, times in slots_by_day.items():
            booked_in_this_day = get_booked_slots(doctor_id, day)
            
            for time_val in times:
                if time_val not in booked_in_this_day:
                    if day not in weekly_schedule:
                        weekly_schedule[day] = []
                    weekly_schedule[day].append(time_val)
                else:
                    print(f"Skipping {day} {time_val} because it is BOOKED.")

        print("=== END FILTERING ===\n")

        feedback_result = DoctorController.get_feedback(doctor_id)
        feedback = feedback_result.get('feedback', []) if feedback_result['success'] else []
        
        return render_template('booking.html', 
                             doctors=doctors, 
                             doctor=selected_doctor, 
                             feedback=feedback,
                             weekly_schedule=weekly_schedule)

    @app.route('/appointments')
    @login_required
    def appointments():
        user_id = session['user']['id']
        if session['user']['role'] == 'patient':
            result = PatientController.get_appointments(user_id)
            return render_template('appointments.html', appointments=result['appointments'], user_role='patient')
        elif session['user']['role'] == 'doctor':
            doc = DoctorController.get_doctor(user_id).get('doctor')
            return render_template('appointments.html', patients=doc.patients if doc else [], user_role='doctor')
        return render_template('appointments.html')

    @app.route('/cancel-appointment', methods=['POST'])
    @login_required
    def cancel_appointment():
        appointment_id = request.form.get('appointment_id')
        from repositories.repository_factory import RepositoryFactory
        appointment_repo = RepositoryFactory.get_appointment_repository()
        appointment = appointment_repo.get_by_id(appointment_id)
        if appointment:
            doctor_id = appointment.doctor_id
            appointment_date = appointment.appointment_date
            appointment_time = appointment.appointment_time
            PatientController.cancel_appointment(appointment_id)
            DoctorController.add_available_time(doctor_id, appointment_date, appointment_time)
        else:
            PatientController.cancel_appointment(appointment_id)
        return redirect(url_for('appointments'))
