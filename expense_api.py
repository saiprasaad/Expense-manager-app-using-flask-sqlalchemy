from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request
from expense import Expense, db
from datetime import datetime
from sqlalchemy import desc

expense_bp = Blueprint('expense', __name__)


@expense_bp.route("/")
def view_expenses():
    expenses = []
    sort_order = request.args.get('order')
    if not sort_order:
        sort_order = 'asc'
    if sort_order == 'asc':
        expenses = Expense.query.order_by(Expense.amount).all()
    else:
        expenses = Expense.query.order_by(desc(Expense.amount)).all()
    return render_template("index.html", expenses = expenses)

@expense_bp.route("/create", methods = ["GET", "POST"])
def create_expense():
    if request.method == "POST":
        print(request.form)
        if 'desc' not in request.form or len(request.form['desc']) == 0 or 'amount' not in request.form or len(request.form['amount']) == 0 or 'date' not in request.form or len(request.form['date']) == 0:
            return render_template("add_expense.html", error="Missing required value") 
        desc = request.form['desc']
        amount = float(request.form['amount'])
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        expense_obj = Expense(desc=desc, amount=amount, date=date)
        db.session.add(expense_obj)
        db.session.commit()
        return redirect(url_for('expense.view_expenses'))
    else:
        return render_template("add_expense.html")

@expense_bp.route("/delete/<id>", methods = ["GET", "POST"])
def delete_expense(id):
    expense_found = Expense.query.filter_by(id=id).first()
    if expense_found:
        Expense.query.filter_by(id=id).delete()
        db.session.commit()
    return redirect(url_for("expense.view_expenses"))

@expense_bp.route("/update/<id>", methods = ["GET", "POST"])
def update_expense(id):
    if request.method == "GET":
        expense_found = Expense.query.filter_by(id=id).first()
        return render_template("edit_expense.html", expense=expense_found )
    else:
        if 'desc' not in request.form or len(request.form['desc']) == 0 or 'amount' not in request.form or len(request.form['amount']) == 0 or 'date' not in request.form or len(request.form['date']) == 0:
            return render_template("edit_expense.html", error="Missing required value") 
        desc = request.form['desc']
        amount = float(request.form['amount'])
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        expense_found = Expense.query.filter_by(id=id).first()
        if expense_found:
            expense_found.desc = desc
            expense_found.amount = amount
            expense_found.date = date
            db.session.commit()
            return redirect(url_for("expense.view_expenses"))
        
@expense_bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@expense_bp.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500
