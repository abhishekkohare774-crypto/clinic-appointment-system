import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='clinic.db'):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        """Get a database connection"""
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Initialize the database with tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create Patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                date_of_birth TEXT,
                gender TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create Doctors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specialization TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                license_number TEXT UNIQUE NOT NULL,
                available_hours TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create Appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                reason TEXT,
                status TEXT DEFAULT 'Scheduled',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
            )
        ''')

        conn.commit()
        conn.close()

    # PATIENT OPERATIONS
    def add_patient(self, name, phone, email, dob, gender, address):
        """Add a new patient"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO patients (name, phone, email, date_of_birth, gender, address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, phone, email, dob, gender, address))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding patient: {e}")
            return False
        finally:
            conn.close()

    def get_all_patients(self):
        """Get all patients"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patients ORDER BY name')
        patients = cursor.fetchall()
        conn.close()
        return patients

    def get_patient(self, patient_id):
        """Get a specific patient"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
        patient = cursor.fetchone()
        conn.close()
        return patient

    def update_patient(self, patient_id, name, phone, email, dob, gender, address):
        """Update patient information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE patients
                SET name = ?, phone = ?, email = ?, date_of_birth = ?, gender = ?, address = ?
                WHERE patient_id = ?
            ''', (name, phone, email, dob, gender, address, patient_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating patient: {e}")
            return False
        finally:
            conn.close()

    def delete_patient(self, patient_id):
        """Delete a patient"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM patients WHERE patient_id = ?', (patient_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting patient: {e}")
            return False
        finally:
            conn.close()

    # DOCTOR OPERATIONS
    def add_doctor(self, name, specialization, phone, email, license_number, available_hours):
        """Add a new doctor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO doctors (name, specialization, phone, email, license_number, available_hours)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, specialization, phone, email, license_number, available_hours))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding doctor: {e}")
            return False
        finally:
            conn.close()

    def get_all_doctors(self):
        """Get all doctors"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM doctors ORDER BY name')
        doctors = cursor.fetchall()
        conn.close()
        return doctors

    def get_doctor(self, doctor_id):
        """Get a specific doctor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM doctors WHERE doctor_id = ?', (doctor_id,))
        doctor = cursor.fetchone()
        conn.close()
        return doctor

    def update_doctor(self, doctor_id, name, specialization, phone, email, license_number, available_hours):
        """Update doctor information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE doctors
                SET name = ?, specialization = ?, phone = ?, email = ?, license_number = ?, available_hours = ?
                WHERE doctor_id = ?
            ''', (name, specialization, phone, email, license_number, available_hours, doctor_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating doctor: {e}")
            return False
        finally:
            conn.close()

    def delete_doctor(self, doctor_id):
        """Delete a doctor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM doctors WHERE doctor_id = ?', (doctor_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting doctor: {e}")
            return False
        finally:
            conn.close()

    # APPOINTMENT OPERATIONS
    def add_appointment(self, patient_id, doctor_id, appointment_date, appointment_time, reason, notes):
        """Add a new appointment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason, notes, status)
                VALUES (?, ?, ?, ?, ?, ?, 'Scheduled')
            ''', (patient_id, doctor_id, appointment_date, appointment_time, reason, notes))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding appointment: {e}")
            return False
        finally:
            conn.close()

    def get_all_appointments(self):
        """Get all appointments"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, p.name as patient_name, d.name as doctor_name, d.specialization
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_date, a.appointment_time
        ''')
        appointments = cursor.fetchall()
        conn.close()
        return appointments

    def get_appointment(self, appointment_id):
        """Get a specific appointment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, p.name as patient_name, d.name as doctor_name, d.specialization
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.appointment_id = ?
        ''', (appointment_id,))
        appointment = cursor.fetchone()
        conn.close()
        return appointment

    def get_patient_appointments(self, patient_id):
        """Get all appointments for a patient"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, p.name as patient_name, d.name as doctor_name, d.specialization
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.patient_id = ?
            ORDER BY a.appointment_date, a.appointment_time
        ''', (patient_id,))
        appointments = cursor.fetchall()
        conn.close()
        return appointments

    def get_doctor_appointments(self, doctor_id):
        """Get all appointments for a doctor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, p.name as patient_name, d.name as doctor_name, d.specialization
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.doctor_id = ?
            ORDER BY a.appointment_date, a.appointment_time
        ''', (doctor_id,))
        appointments = cursor.fetchall()
        conn.close()
        return appointments

    def update_appointment(self, appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status, notes):
        """Update appointment information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE appointments
                SET patient_id = ?, doctor_id = ?, appointment_date = ?, appointment_time = ?, reason = ?, status = ?, notes = ?
                WHERE appointment_id = ?
            ''', (patient_id, doctor_id, appointment_date, appointment_time, reason, status, notes, appointment_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating appointment: {e}")
            return False
        finally:
            conn.close()

    def update_appointment_status(self, appointment_id, status):
        """Update appointment status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE appointments SET status = ? WHERE appointment_id = ?', (status, appointment_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating appointment status: {e}")
            return False
        finally:
            conn.close()

    def delete_appointment(self, appointment_id):
        """Delete an appointment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM appointments WHERE appointment_id = ?', (appointment_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting appointment: {e}")
            return False
        finally:
            conn.close()

    def get_appointments_by_date(self, appointment_date):
        """Get all appointments for a specific date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, p.name as patient_name, d.name as doctor_name, d.specialization
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.appointment_date = ?
            ORDER BY a.appointment_time
        ''', (appointment_date,))
        appointments = cursor.fetchall()
        conn.close()
        return appointments

    def check_doctor_availability(self, doctor_id, appointment_date, appointment_time):
        """Check if doctor is available at a specific date and time"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM appointments
            WHERE doctor_id = ? AND appointment_date = ? AND appointment_time = ? AND status != 'Cancelled'
        ''', (doctor_id, appointment_date, appointment_time))
        count = cursor.fetchone()[0]
        conn.close()
        return count == 0
