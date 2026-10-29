# Clinexa

**Clinexa** is a Clinical Management System designed to streamline interactions between doctors and patients. It features a complete appointment booking engine, role-based dashboards, and a custom CSV-based persistence layer, developed for the CSAI203 Software Engineering course.

## Project Architecture

The application implements a strict **MVC (Model-View-Controller)** architecture with a **Repository Pattern** to decouple business logic from data access.

* **src/controllers/**: Orchestrates logic between the UI and data models.
* **src/repositories/**: Handles direct interactions with the CSV database.
* **src/models/**: Python classes representing core entities (Doctor, Patient, Appointment).
* **src/data/**: Flat-file database storage containing all system records in CSV format.
* **src/core/**: Core system utilities including Authentication and CSV management.

## Key Features

* **Role-Based Access**:
    * **Doctors**: Manage schedules, view appointments, and upload reports.
    * **Patients**: Book appointments, view medical reports, and rate/review doctors.
* **Appointment System**: Full lifecycle management (Booking, Scheduling, History).
* **Feedback Loop**: Integrated rating system stored in feedback.csv.
* **Data Persistence**: Custom-built CSV manager ensuring data integrity.
* **Secure Authentication**: Hashed credentials and session management.

## Project Documentation

Detailed documentation regarding the system design, requirements, and usage instructions can be found in the docs/ folder of this repository.

| Document | Path | Description |
| :--- | :--- | :--- |
| **User Manual** | docs/Clinexa User Manual | Step-by-step guide for Patients and Doctors. |
| **System Design** | docs/CSAI203_Design_Team26.pdf | UML diagrams, architecture, and design patterns. |
| **SRS** | docs/CSAI203_SRS_Team26.pdf | Functional & non-functional requirements. |

## Default Login Credentials

Use these credentials to test the application's different roles.

| Role | Email | Password |
| :--- | :--- | :--- |
| **Doctor** | Clinexa_Doctor@clinexa.eg | Doctor_Password_123 |

## Tech Stack

* **Language**: Python 3.11
* **Framework**: Flask
* **Frontend**: HTML5, CSS3, JavaScript
* **Containerization**: Docker
* **CI/CD**: GitHub Actions

## Installation & Setup

We recommend running Clinexa by pulling the pre-built image from Docker Hub.

### Prerequisites
* Docker Desktop or Docker Engine installed.
* Git.

### Step 1: Clone the Repository
```bash
git clone [https://github.com/r4g4b/clinexa.git](https://github.com/r4g4b/clinexa.git)
cd clinexa

```

### Step 2: Pull the Docker Image

Instead of building manually, pull the latest verified version directly from the cloud.

```bash
docker pull j4b4l/clinexa:latest

```

### Step 3: Run the Application

Start the container and map port 5000.

```bash
docker run -p 5000:5000 j4b4l/clinexa:latest

```

*(Optional: To keep data saved locally, map the data folder)*:

```bash
docker run -p 5000:5000 -v $(pwd)/src/data:/app/src/data j4b4l/clinexa:latest

```

### Alternative: Build Locally

If you prefer to build the image from source on your machine:

```bash
docker build -t clinexa-app .
docker run -p 5000:5000 clinexa-app

```

### Step 4: Access the App

Open your browser and navigate to: http://localhost:5000

## Testing

The project maintains a high standard of code quality with a full test suite.

**Run all tests (Local Python):**

```bash
pip install -r requirements.txt
python run_tests_dispatch.py all

```

**Run tests inside Docker:**

```bash
docker build -t clinexa-test .
docker run clinexa-test python run_tests_dispatch.py all

```

## Authors

**CSAI203 - Team 26**
Contact: s-mosab.gabal@zewailcity.edu.eg
