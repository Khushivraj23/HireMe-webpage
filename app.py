from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from database import init_db
from pythonfiles.report import generate_report
from pythonfiles.Student_reset_pass import update_student_password
from pythonfiles.rec_forgotpassword import update_password
from pythonfiles.recruiter_register import register_recruiter
from pythonfiles.create_job import add_job
from pythonfiles.recruiter_home import get_all_jobs
from pythonfiles.Student_home import apply_job, fetch_job_details, get_jobs_by_application_status
from pythonfiles.recruiterslogin import check_recruiter_login
from pythonfiles.students_login import check_student_login
from pythonfiles.Students_register import register_student
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = '2345'
CORS(app)

# Initialize the database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

# ---------------------- STUDENT REGISTRATION ----------------------
@app.route('/student_register', methods=['POST'])
def student_register():
    data = request.get_json()
    return register_student(
        data.get('usn'),
        data.get('name'),
        data.get('email'),
        data.get('password'),
        data.get('confirm_password'),
        data.get('skills'),
        data.get('branch'),
        data.get('college_name'),
        data.get('phone_number')
    )

@app.route('/student_register')
def student_register_page():
    return render_template('student_register.html')

# ---------------------- RECRUITER REGISTRATION ----------------------
@app.route('/recruiter_register', methods=['POST'])
def recruiter_register():
    data = request.get_json()
    return register_recruiter(
        data.get('username'),
        data.get('firstname'),
        data.get('lastname'),
        data.get('email'),
        data.get('password'),
        data.get('confirm_password'),
        data.get('company'),
        data.get('phone_number')
    )

@app.route('/recruiter_register')
def recruiter_register_page():
    return render_template('recruiter_register.html')

# ---------------------- CREATE JOB ----------------------
@app.route('/api/jobs', methods=['POST'])
def api_add_job():
    data = request.get_json()
    add_job(
        data.get('job_role'),
        data.get('company'),
        data.get('package'),
        data.get('job_description')
    )
    return jsonify({'success': True})

@app.route('/create_job_page')
def create_job_page():
    return render_template('create_job.html')

# ---------------------- RECRUITER LOGIN ----------------------
@app.route('/recruiter_login', methods=['POST'])
def recruiter_login():
    data = request.get_json()
    return check_recruiter_login(data.get('username'), data.get('password'))

@app.route('/recruiter_login')
def recruiter_login_page():
    return render_template('recruiter_login.html')

# ---------------------- RECRUITER HOME ----------------------
@app.route('/recruiter_home')
def recruiter_home():
    return render_template('recruiter_home.html')

@app.route('/recruiter/job/<int:job_id>')
def recruiter_job_page(job_id):
    return render_template('recruiter_job_details.html')

@app.route('/api/jobs', methods=['GET'])
def api_get_jobs():
    jobs = get_all_jobs()
    return jsonify(jobs)

# ---------------------- STUDENT LOGIN ----------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return check_student_login(data.get('usn'), data.get('password'))

@app.route('/student_login')
def student_login():
    return render_template('student_login.html')

# ---------------------- STUDENT HOME ----------------------
@app.route('/student_home')
def student_home():
    return render_template('student_home.html')

@app.route('/api/apply_job', methods=['POST'])
def apply_job_route():
    data = request.get_json()
    usn = session.get('usn')
    job_id = data.get('job_id')
    apply_job(usn, job_id)
    return jsonify({'success': True})

@app.route('/api/jobs_by_status', methods=['GET'])
def api_get_jobs_by_status():
    usn = session.get('usn')
    if not usn:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(get_jobs_by_application_status(usn))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('student_login'))

@app.route('/api/job_details/<int:job_id>')
def job_details(job_id):
    job = fetch_job_details(job_id)
    if job:
        return jsonify(job)
    return jsonify({'error': 'Job not found'}), 404

# ---------------------- JOB DETAILS PAGE ----------------------
@app.route('/job/<int:job_id>')
def job_page(job_id):
    return render_template('job_details.html')

# ---------------------- RECRUITER FORGOT PASSWORD ----------------------
@app.route('/rec_forgot_password')
def forgot_password_page():
    return render_template('rec_forgot_password.html')

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    if new_password != confirm_password:
        return jsonify({'success': False, 'message': 'Passwords do not match'})
    return update_password(username, new_password)

# ---------------------- STUDENT FORGOT PASSWORD ----------------------
@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    usn = data.get('usn')
    email = data.get('email')
    new_password = data.get('new_password')
    if not usn or not email or not new_password:
        return jsonify({'success': False, 'message': 'Please fill all the fields'}), 400
    return update_student_password(usn, email, new_password)

@app.route('/reset-password-page')
def reset_password_page():
    return render_template('student_reset_password.html')

# ---------------------- REPORT PAGE ----------------------
@app.route('/report')
def report_page():
    return render_template('report.html')

@app.route('/api/report')
def api_report_data():
    return jsonify(generate_report())

# ---------------------- RUN FLASK APP ----------------------
if __name__ == '__main__':
    app.run(debug=True)