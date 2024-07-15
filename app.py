from flask import Flask, render_template, redirect, url_for, jsonify, request
from sqlalchemy import desc
from expense import Expense, db
from datetime import datetime
from expense_api import expense_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///expense.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_blueprint(expense_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)