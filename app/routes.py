from flask import render_template, redirect, url_for, request
from app import app, db
from app.models import JobApplication

@app.route('/')
def index():
    job_applications = JobApplication.query.all()
    return render_template('index.html', job_applications=job_applications)

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        company = request.form['company']  
        position = request.form['position']
        date_applied = request.form['date_applied']
        status = request.form['status']
        notes = request.form.get('notes', '')

        new_application = JobApplication(company=company, position=position, date_applied=date_applied, status=status, notes=notes)  
        db.session.add(new_application)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('add.html')
