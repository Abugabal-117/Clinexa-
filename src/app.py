import sys
import os
from flask import Flask
import secrets

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from routes.core_routes import register_core_routes
from routes.auth_routes import register_auth_routes
from routes.patient_routes import register_patient_routes
from routes.doctor_routes import register_doctor_routes
from routes.profile_routes import register_profile_routes

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

register_core_routes(app)
register_auth_routes(app)
register_patient_routes(app)
register_doctor_routes(app)
register_profile_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
