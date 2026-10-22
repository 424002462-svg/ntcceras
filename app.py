import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'ceras_secret_key_ntc_2026'

USERS = {
    "42400001": {
        "password": "newStudent1",
        "role": "student",
        "name": "Aaron De Guzman",
        "year_level": "BSIT 3.6",
        "college": "School of Information Technology",
        "group": "BSIT"
    },
    "42400002": {
        "password": "password123",
        "role": "student",
        "name": "Prince Jariel Cagata",
        "year_level": "BSIT 3.6",
        "college": "School of Information Technology",
        "group": "BSIT"
    },
    "42400003": {
        "password": "password123",
        "role": "student",
        "name": "Kently Gevrieyl Licop",
        "year_level": "BSIT 3.6",
        "college": "School of Information Technology",
        "group": "BSIT"
    },
    "42400004": {
        "password": "password123",
        "role": "student",
        "name": "Gherremy Verde",
        "year_level": "BSIT 3.6",
        "college": "School of Information Technology",
        "group": "BSIT" 
    },
    "42400005": {
        "password": "password123",
        "role": "student",
        "name": "Jacob Ramos",
        "year_level": "BSIT 3.6",
        "college": "School of Information Technology",
        "group": "BSIT"
    },
    "42400006": {
        "password": "password123",
        "role": "student",
        "name": "Chris Justine Pialan",
        "year_level": "BSIT 3.6",
        "college": "School of Information Technology",
        "group": "BSIT"
    },
    "42400007": {
        "password": "password123",
        "role": "student",
        "name": "Adrian Jhames Aguilar",
        "year_level": "BSIT 3.6",
        "college": "School of Information Technology",
        "group": "BSIT"
    },
    "Admin1": {
        "password": "admin123",
        "role": "admin",
        "name": "Mr. Entrolizo Eon",
        "college": "All"
    }
}

EVENTS = {
    "EVT001": {
        "id": "EVT001",
        "title": "Software Engineering Seminar",
        "description": "Comprehensive workshop on UML Modelling, Architecture, and Requirements Analysis.",
        "date": "2026 11 15",
        "time_start": "09:00",
        "time_end": "12:00",
        "location": "NTC Auditorium",
        "capacity": 5,
        "eligibility_year": "BSIT 3",
        "eligibility_college": "School of Information Technology",
        "registered": ["42400002", "42400003", "42400004", "42400005", "42400006"],
        "waiting_list": ["42400007"],
        "attendance": {
            "42400002": True,
            "42400003": True,
            "42400004": False,
            "42400005": True,
            "42400006": False
        }
    },
    "EVT002": {
        "id": "EVT002",
        "title": "IT Cyber Security & Privacy Forum",
        "description": "Interactive talk on student data protection and secure system access rules.",
        "date": "2026 11 18",
        "time_start": "13:00",
        "time_end": "16:00",
        "location": "NTC AVR Room 301",
        "capacity": 30,
        "eligibility_year": "All",
        "eligibility_college": "School of Information Technology",
        "registered": ["42400001", "42400002", "42400007"],
        "waiting_list": [],
        "attendance": {
            "42400001": True,
            "42400002": False,
            "42400007": True
        }
    },
    "EVT003": {
        "id": "EVT003",
        "title": "NTC General Student Assembly",
        "description": "All college campus gathering for annual academic activity updates.",
        "date": "2026 11 20",
        "time_start": "08:00",
        "time_end": "11:00",
        "location": "NTC Gymnasium",
        "capacity": 100,
        "eligibility_year": "All",
        "eligibility_college": "All",
        "registered": ["42400001", "42400003", "42400004", "42400005"],
        "waiting_list": [],
        "attendance": {
            "42400001": True,
            "42400003": True,
            "42400004": False,
            "42400005": True
        }
    },
    "EVT004": {
        "id": "EVT004",
        "title": "UI UX & Web Systems Workshop",
        "description": "Hands on web interfaces development and usability design.",
        "date": "2026 11 25",
        "time_start": "10:00",
        "time_end": "15:00",
        "location": "IT Computer Lab 2",
        "capacity": 25,
        "eligibility_year": "BSIT 3",
        "eligibility_college": "School of Information Technology",
        "registered": ["42400006", "42400007"],
        "waiting_list": [],
        "attendance": {}
    }
}

def check_schedule_conflict(username, new_event_id):
    new_evt = EVENTS[new_event_id]
    new_start = datetime.datetime.strptime(f"{new_evt['date']} {new_evt['time_start']}", "%Y %m %d %H:%M")
    new_end = datetime.datetime.strptime(f"{new_evt['date']} {new_evt['time_end']}", "%Y %m %d %H:%M")

    for evt_id, evt in EVENTS.items():
        if evt_id != new_event_id and username in evt['registered']:
            existing_start = datetime.datetime.strptime(f"{evt['date']} {evt['time_start']}", "%Y %m %d %H:%M")
            existing_end = datetime.datetime.strptime(f"{evt['date']} {evt['time_end']}", "%Y %m %d %H:%M")

            if max(new_start, existing_start) < min(new_end, existing_end):
                return True, evt['title']
    return False, None

def promote_from_waiting_list(event_id):
    evt = EVENTS[event_id]
    if len(evt['registered']) < evt['capacity'] and len(evt['waiting_list']) > 0:
        promoted_student = evt['waiting_list'].pop(0)
        evt['registered'].append(promoted_student)
        return promoted_student
    return None

@app.route('/')
def index():
    if 'user' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('student_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = USERS.get(username)
        if user and user['password'] == password:
            session['user'] = username
            session['role'] = user['role']
            session['name'] = user['name']
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials. Please check your Email ID and Password.", "danger")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for('login'))

@app.route('/student/dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    
    student_info = USERS[session['user']]
    return render_template('student_dashboard.html', events=EVENTS, student=student_info, users=USERS)

@app.route('/register_event/<event_id>')
def register_event(event_id):
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    
    username = session['user']
    student = USERS[username]
    evt = EVENTS.get(event_id)

    if not evt:
        flash("Event not found.", "danger")
        return redirect(url_for('student_dashboard'))

    if username in evt['registered']:
        flash("You are already registered for this event.", "warning")
        return redirect(url_for('student_dashboard'))

    has_conflict, conflicting_title = check_schedule_conflict(username, event_id)
    if has_conflict:
        flash(f"Schedule Conflict: You are already registered for '{conflicting_title}' during this time schedule.", "danger")
        return redirect(url_for('student_dashboard'))

    if evt['eligibility_college'] != "All" and evt['eligibility_college'] != student['college']:
        flash(f"Ineligible: This event is restricted to students under {evt['eligibility_college']}.", "danger")
        return redirect(url_for('student_dashboard'))

    if len(evt['registered']) < evt['capacity']:
        evt['registered'].append(username)
        flash("Registration successful!", "success")
    else:
        if username not in evt['waiting_list']:
            evt['waiting_list'].append(username)
            flash("Event capacity is full. You have been placed on the Waiting List.", "info")
        else:
            flash("You are already on the waiting list.", "warning")

    return redirect(url_for('student_dashboard'))

@app.route('/cancel_registration/<event_id>')
def cancel_registration(event_id):
    if session.get('role') != 'student':
        return redirect(url_for('login'))

    username = session['user']
    evt = EVENTS.get(event_id)

    if evt:
        if username in evt['registered']:
            evt['registered'].remove(username)
            if username in evt['attendance']:
                del evt['attendance'][username]
            flash("Registration cancelled successfully.", "info")
            promoted = promote_from_waiting_list(event_id)
            if promoted:
                promoted_name = USERS[promoted]['name']
                flash(f"Slot opened! {promoted_name} was automatically promoted from the waiting list.", "success")
        elif username in evt['waiting_list']:
            evt['waiting_list'].remove(username)
            flash("Removed from waiting list.", "info")

    return redirect(url_for('student_dashboard'))

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_id = f"EVT{len(EVENTS)+1:03d}"
        EVENTS[new_id] = {
            "id": new_id,
            "title": request.form['title'],
            "description": request.form['description'],
            "date": request.form['date'],
            "time_start": request.form['time_start'],
            "time_end": request.form['time_end'],
            "location": request.form['location'],
            "capacity": int(request.form['capacity']),
            "eligibility_year": request.form['eligibility_year'],
            "eligibility_college": request.form['eligibility_college'],
            "registered": [],
            "waiting_list": [],
            "attendance": {}
        }
        flash(f"Event '{request.form['title']}' created successfully!", "success")

    return render_template('admin_dashboard.html', events=EVENTS, users=USERS)

@app.route('/admin/attendance/<event_id>', methods=['GET', 'POST'])
def manage_attendance(event_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    evt = EVENTS.get(event_id)
    if request.method == 'POST':
        target_username = request.form['username']
        is_attended = request.form.get('attended') == 'yes'
        
        evt['attendance'][target_username] = is_attended
        student_name = USERS[target_username]['name']
        status_txt = "Attended Checked" if is_attended else "Not Attended Blank"
        flash(f"Attendance status for {student_name} set to: {status_txt}.", "success")

    return render_template('scan_qr.html', event=evt, users=USERS)

@app.route('/admin/reports')
def view_reports():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('reports.html', events=EVENTS, users=USERS)

if __name__ == '__main__':
    app.run(debug=True)
