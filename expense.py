from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(100))
    amount = db.Column(db.Float)
    date = db.Column(db.Date)
    def __init__(self, desc, amount, date):
        self.desc = desc
        self.amount = amount
        self.date = date