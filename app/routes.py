from flask import render_template, redirect, url_for, request, flash, get_flashed_messages
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db
from app.models import JobApplication, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import make_response

@app.after_request
def add_cache_control(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.context_processor
def make_template_context():
    return dict(get_flashed_messages=get_flashed_messages)

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', 'date')
    
    job_applications = []
    if current_user.is_authenticated:
        query = JobApplication.query.filter_by(user_id=current_user.id)
        
        if sort_by == 'company':
            query = query.order_by(JobApplication.company)
        else:
            query = query.order_by(JobApplication.date_applied.desc())
            
        job_applications = query.paginate(page=page, per_page=9)
    
    return render_template('index.html', job_applications=job_applications)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please login.', 'alert-success-popup')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful.', 'alert-success-popup')
            return redirect(url_for('index'))

        flash('Login failed. Check your username and/or password and try again.', 'alert-danger-popup')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'alert-success-popup')
    return redirect(url_for('login'))

@login_required
@app.route('/add', methods=['GET', 'POST'])
def add():
    user_id = current_user.id
    page = request.args.get('page', 1, type=int)

    if request.method == 'POST':
        company = request.form['company']
        position = request.form['position']
        date_applied = request.form['date_applied']
        status = request.form['status']
        notes = request.form.get('notes', '')

        new_application = JobApplication(company=company, position=position, date_applied=date_applied, status=status, notes=notes, user_id=user_id)
        db.session.add(new_application)
        db.session.commit()

        total_items = JobApplication.query.filter_by(user_id=current_user.id).count()
        
      
        page = (total_items + 8) // 9 

        flash('Job application added successfully.', 'alert-success-popup')
        return redirect(url_for('index', page=page))

    return render_template('add.html')



@app.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update(id):
    job_application = JobApplication.query.get_or_404(id)

    if request.method == 'POST':
        job_application.company = request.form['company']
        job_application.position = request.form['position']
        job_application.date_applied = request.form['date_applied']
        job_application.status = request.form['status']
        job_application.notes = request.form.get('notes', '')

        db.session.commit()

        flash('Job application updated successfully.', 'alert-success-popup')
        return redirect(url_for('index'))

    return render_template('update.html', job_application=job_application)

@login_required
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', 'date')
    job_application = JobApplication.query.get_or_404(id)

    db.session.delete(job_application)
    db.session.commit()

    total_remaining = JobApplication.query.filter_by(user_id=current_user.id).count()
    total_pages = -(-total_remaining // 9)  

    if page > total_pages:
        page = total_pages if total_pages else 1

    flash('Job application deleted successfully.', 'alert-success-popup')
    return redirect(url_for('index', page=page, sort_by=sort_by))



