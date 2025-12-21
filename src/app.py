from flask import Flask, render_template, request, redirect, url_for, session, flash
from controllers.user_controller import UserController
from controllers.patient_controller import PatientController
from controllers.doctor_controller import DoctorController
from controllers.auth_utils import login_required, patient_required, refresh_session_user
import secrets
import csv
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def get_absolute_path(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'data', filename)

def clean_str(val):
    if val is None:
        return ""
    return str(val).strip()

def get_booked_slots(doctor_id, day_name):
    booked_times = []
    file_path = get_absolute_path('appointments.csv')
    
    target_doc = clean_str(doctor_id)
    target_day = clean_str(day_name)

    print(f"\n--- Searching bookings for Day: {target_day} ---")

    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_doc = clean_str(row.get('doctor_id'))
                row_date = clean_str(row.get('appointment_date'))
                row_time = clean_str(row.get('appointment_time'))
                row_status = clean_str(row.get('status'))

                if (row_doc == target_doc and 
                    row_date == target_day and 
                    row_status != 'cancelled'):
                    
                    booked_times.append(row_time)
                    print(f"Found BOOKED slot: {row_time}")
                    
    except Exception as e:
        print(f"Error reading appointments: {e}")
        
    return booked_times

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

def handle_login():
    return redirect(url_for('login'))

def handle_dashboard():
    return redirect(url_for('dashboard'))

def get_login_page():
    return render_template('login.html')

def get_signup_page():
    return render_template('signup.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
    session.clear()
    UserController.logout()
    return redirect(url_for('home'))

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

@app.route('/schedule-management', methods=['GET', 'POST'])
@login_required
def schedule_management():
    if session['user']['role'] != 'doctor': return redirect(url_for('dashboard'))
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

@app.route('/doctor-profile', defaults={'doctor_id': None})
@app.route('/doctor-profile/<doctor_id>')
@login_required
def doctor_profile(doctor_id):
    if not doctor_id:
        if session['user']['role'] == 'doctor': doctor_id = session['user']['id']
        else:
            docs = DoctorController.get_all_doctors()['doctors']
            doctor_id = docs[0].user_id if docs else None
    if not doctor_id: return redirect(url_for('dashboard'))
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

@app.route('/patient-report', methods=['GET', 'POST'])
@login_required
def patient_report():
    if session['user']['role'] != 'doctor': return redirect(url_for('dashboard'))
    doctor_id = session['user']['id']
    if request.method == 'POST':
        DoctorController.create_report(doctor_id, request.form.get('patient_id'), request.form.get('patient_name_hidden'), request.form.get('report_details'))
        return redirect(url_for('patient_report'))
    patients = DoctorController.get_all_patients()
    reports = DoctorController.get_doctor_reports(doctor_id).get('reports', [])
    return render_template('patient-report.html', patients=patients, reports=reports)

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

@app.route('/remove-patient/<patient_id>', methods=['POST'])
@login_required
def remove_patient(patient_id):
    DoctorController.remove_patient(session['user']['id'], patient_id)
    return redirect(url_for('appointments'))

@app.route('/about-doctor')
def about_doctor():
    doctors_result = DoctorController.get_all_doctors()
    doctors = doctors_result.get('doctors', []) if doctors_result['success'] else []
    doctor = doctors[0] if doctors else None
    return render_template('about-doctor.html', doctor=doctor)
@app.route('/forgot-password')
def forgot_password(): return render_template('forgot-password.html')
@app.route('/reset-password')
def reset_password(): return render_template('reset-password.html')
@app.route('/rating', methods=['GET', 'POST'])
@patient_required
def rating():
    doctor_id = request.args.get('doctor_id') or request.form.get('doctor_id')
    if request.method == 'POST':
        rating_value = request.form.get('rating')
        comment = request.form.get('comment')
        
        if rating_value and doctor_id:
            PatientController.submit_feedback(session['user']['id'], doctor_id, int(rating_value), comment)
            flash('Thank you for your feedback!', 'success')
            return redirect(url_for('about_doctor'))
    
    doctor = None
    if doctor_id:
        doctor_result = DoctorController.get_doctor(doctor_id)
        doctor = doctor_result.get('doctor') if doctor_result['success'] else None
    
    return render_template('rating.html', doctor=doctor)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
