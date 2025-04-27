from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# --- Database Connection ---
def get_db_connection():
    conn = sqlite3.connect('healthcare.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Home ---
@app.route('/')
def home():
    return render_template('home.html')

# --- USERS ---
@app.route('/users')
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('users.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        contact_info = request.form['contact_info']
        email = request.form['email']
        conn = get_db_connection()
        conn.execute('INSERT INTO users (name, contact_info, email) VALUES (?, ?, ?)', (name, contact_info, email))
        conn.commit()
        conn.close()
        return redirect(url_for('users'))
    return render_template('add_user.html')

@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        contact_info = request.form['contact_info']
        email = request.form['email']
        conn.execute('UPDATE users SET name = ?, contact_info = ?, email = ? WHERE user_id = ?', (name, contact_info, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for('users'))
    conn.close()
    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE user_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('users'))

# --- DOCTORS ---
@app.route('/doctors')
def doctors():
    conn = get_db_connection()
    doctors = conn.execute('''
        SELECT d.doctor_id, d.name, d.email, s.specialization_name
        FROM doctors d
        LEFT JOIN specializations s ON d.specialization_id = s.specialization_id
    ''').fetchall()
    conn.close()
    return render_template('doctors.html', doctors=doctors)

@app.route('/delete_doctor/<int:id>')
def delete_doctor(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM doctors WHERE doctor_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('doctors'))

# --- PHARMACIES ---
@app.route('/pharmacies')
def pharmacies():
    conn = get_db_connection()
    pharmacies = conn.execute('SELECT * FROM pharmacies').fetchall()
    conn.close()
    return render_template('pharmacies.html', pharmacies=pharmacies)

@app.route('/delete_pharmacy/<int:id>')
def delete_pharmacy(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM pharmacies WHERE pharmacy_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('pharmacies'))

# --- APPOINTMENTS ---
@app.route('/appointments')
def appointments():
    conn = get_db_connection()
    appointments = conn.execute('''
        SELECT a.appointment_id, u.name AS user_name, d.name AS doctor_name, a.appointment_date
        FROM appointments a
        LEFT JOIN users u ON a.user_id = u.user_id
        LEFT JOIN doctors d ON a.doctor_id = d.doctor_id
    ''').fetchall()
    conn.close()
    return render_template('appointments.html', appointments=appointments)

@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    doctors = conn.execute('SELECT * FROM doctors').fetchall()
    if request.method == 'POST':
        user_id = request.form['user_id']
        doctor_id = request.form['doctor_id']
        appointment_date = request.form['appointment_date']
        conn.execute('INSERT INTO appointments (user_id, doctor_id, appointment_date) VALUES (?, ?, ?)',
                     (user_id, doctor_id, appointment_date))
        conn.commit()
        conn.close()
        return redirect(url_for('appointments'))
    conn.close()
    return render_template('add_appointment.html', users=users, doctors=doctors)

@app.route('/edit_appointment/<int:id>', methods=['GET', 'POST'])
def edit_appointment(id):
    conn = get_db_connection()
    appointment = conn.execute('SELECT * FROM appointments WHERE appointment_id = ?', (id,)).fetchone()
    users = conn.execute('SELECT * FROM users').fetchall()
    doctors = conn.execute('SELECT * FROM doctors').fetchall()
    if request.method == 'POST':
        user_id = request.form['user_id']
        doctor_id = request.form['doctor_id']
        appointment_date = request.form['appointment_date']
        conn.execute('UPDATE appointments SET user_id = ?, doctor_id = ?, appointment_date = ? WHERE appointment_id = ?',
                     (user_id, doctor_id, appointment_date, id))
        conn.commit()
        conn.close()
        return redirect(url_for('appointments'))
    conn.close()
    return render_template('edit_appointment.html', appointment=appointment, users=users, doctors=doctors)

@app.route('/delete_appointment/<int:id>')
def delete_appointment(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM appointments WHERE appointment_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('appointments'))

# --- PRESCRIPTIONS ---
@app.route('/prescriptions')
def prescriptions():
    conn = get_db_connection()
    prescriptions = conn.execute('''
        SELECT p.prescription_id, u.name AS user_name, d.name AS doctor_name, ph.name AS pharmacy_name, p.prescription_date
        FROM prescriptions p
        LEFT JOIN users u ON p.user_id = u.user_id
        LEFT JOIN doctors d ON p.doctor_id = d.doctor_id
        LEFT JOIN pharmacies ph ON p.pharmacy_id = ph.pharmacy_id
    ''').fetchall()
    conn.close()
    return render_template('prescriptions.html', prescriptions=prescriptions)

@app.route('/add_prescription', methods=['GET', 'POST'])
def add_prescription():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    doctors = conn.execute('SELECT * FROM doctors').fetchall()
    pharmacies = conn.execute('SELECT * FROM pharmacies').fetchall()
    if request.method == 'POST':
        user_id = request.form['user_id']
        doctor_id = request.form['doctor_id']
        pharmacy_id = request.form['pharmacy_id']
        prescription_date = request.form['prescription_date']
        conn.execute('INSERT INTO prescriptions (user_id, doctor_id, pharmacy_id, prescription_date) VALUES (?, ?, ?, ?)',
                     (user_id, doctor_id, pharmacy_id, prescription_date))
        conn.commit()
        conn.close()
        return redirect(url_for('prescriptions'))
    conn.close()
    return render_template('add_prescription.html', users=users, doctors=doctors, pharmacies=pharmacies)

@app.route('/edit_prescription/<int:id>', methods=['GET', 'POST'])
def edit_prescription(id):
    conn = get_db_connection()
    prescription = conn.execute('SELECT * FROM prescriptions WHERE prescription_id = ?', (id,)).fetchone()
    users = conn.execute('SELECT * FROM users').fetchall()
    doctors = conn.execute('SELECT * FROM doctors').fetchall()
    pharmacies = conn.execute('SELECT * FROM pharmacies').fetchall()
    if request.method == 'POST':
        user_id = request.form['user_id']
        doctor_id = request.form['doctor_id']
        pharmacy_id = request.form['pharmacy_id']
        prescription_date = request.form['prescription_date']
        conn.execute('UPDATE prescriptions SET user_id = ?, doctor_id = ?, pharmacy_id = ?, prescription_date = ? WHERE prescription_id = ?',
                     (user_id, doctor_id, pharmacy_id, prescription_date, id))
        conn.commit()
        conn.close()
        return redirect(url_for('prescriptions'))
    conn.close()
    return render_template('edit_prescription.html', prescription=prescription, users=users, doctors=doctors, pharmacies=pharmacies)

@app.route('/delete_prescription/<int:id>')
def delete_prescription(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM prescriptions WHERE prescription_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('prescriptions'))

# --- MAIN ---
if __name__ == '__main__':
    app.run(debug=True)
