from flask import render_template, redirect, url_for, request
from app import app, db
from app.models import JobApplication

@app.route('/')
def index():
    sort_by = request.args.get('sort_by')
    
    if sort_by == "company":
        job_applications = JobApplication.query.order_by(JobApplication.company).all()
    elif sort_by == "date":
        job_applications = JobApplication.query.order_by(JobApplication.date_applied.desc()).all()
    else:
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

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    job_application = JobApplication.query.get_or_404(id)
    
    if request.method == 'POST':
        job_application.company = request.form['company']
        job_application.position = request.form['position']
        job_application.date_applied = request.form['date_applied']
        job_application.status = request.form['status']
        job_application.notes = request.form.get('notes', '')
        
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('update.html', job_application=job_application)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    job_application = JobApplication.query.get_or_404(id)
    db.session.delete(job_application)
    db.session.commit()
    return redirect(url_for('index'))




