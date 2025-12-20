import os
import csv

def get_absolute_path(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'src', 'data', filename)

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
