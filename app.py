from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='template')


# Mock student data
students = []

# Mock attendance data
attendance = {}

# Empty list for attendance records at the global level
attendance_records = []

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'user123' and request.form['password'] == 'passkey123':
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

# Dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Add student route
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student = {
            'name': request.form['name'],
            'roll_no': request.form['roll_no'],
            'class': request.form['class'],
            'section': request.form['section'],
            'parent_contact': request.form['parent_contact']
        }
        students.append(student)
        students.sort(key=lambda x: x['name'])
        return redirect(url_for('dashboard'))
    return render_template('add_student.html')

# View database route
@app.route('/view_database')
def view_database():
    return render_template('view_database.html', students=students)

# Remove student route
@app.route('/remove_student/<string:name>')
def remove_student(name):
    global students
    students = [student for student in students if student['name'] != name]
    return redirect(url_for('view_database'))

@app.route('/view_attendance', methods=['GET', 'POST'])
def view_attendance():
    global attendance_records  # access to the global variable
    if request.method == 'POST':
        # Handle form submission for adding attendance
        student_name = request.form['student_name']
        roll_no = request.form['roll_no']
        date = request.form['date']
        attendance = request.form['attendance']
        
        # Add attendance record to the list
        attendance_records.append({'student_name': student_name, 'roll_no': roll_no, 'date': date, 'attendance': attendance})
        
        # Redirect to dashboard after adding attendance
        return redirect(url_for('dashboard'))
    else:
        return render_template('view_attendance.html', attendance_records=attendance_records)

@app.route('/edit_attendance', methods=['GET', 'POST'])
def edit_attendance():
    global attendance_records  # Ensure access to the global variable
    if request.method == 'POST':
        # Handle form submission for editing attendance
        # Logic for editing attendance records
        # Retrieve form data
        student_name = request.form['student_name']
        date = request.form['date']
        attendance = request.form['attendance']

        # Find the attendance record to edit
        for record in attendance_records:
            if record['student_name'] == student_name and record['date'] == date:
                record['attendance'] = attendance
                break
        
        # Redirect to dashboard after editing attendance
        return redirect(url_for('dashboard'))
    else:
        return render_template('edit_attendance.html', attendance_records=attendance_records)


@app.route('/add_attendance', methods=['GET', 'POST'])
def add_attendance():
    global attendance_records  # access to the global variable
    if request.method == 'POST':
        # Handle form submission for adding attendance
        student_name = request.form['student_name']
        roll_no = request.form['roll_no']
        date = request.form['date']
        attendance = request.form['attendance']
        
        # Add attendance record to the list
        attendance_records.append({'student_name': student_name, 'roll_no': roll_no, 'date': date, 'attendance': attendance})
        
        # Redirect to dashboard after adding attendance
        return redirect(url_for('dashboard'))
    else:
        return render_template('add_attendance.html')
    
@app.route('/remove_attendance', methods=['POST'])
def remove_attendance():
    if request.method == 'POST':
        student_name = request.form['student_name']
        date = request.form['date']
        # Logic to remove attendance record with given student name and date
        global attendance_records
        attendance_records = [record for record in attendance_records if not (record['student_name'] == student_name and record['date'] == date)]
        return redirect(url_for('view_attendance'))
    return redirect(url_for('view_attendance'))  # Redirect to view attendance page

    
if __name__ == '__main__':
    app.run(debug=True)
