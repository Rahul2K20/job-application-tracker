from app import db

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150), nullable=False)
    position = db.Column(db.String(150), nullable=False)
    date_applied = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="Pending")
    notes = db.Column(db.Text)
