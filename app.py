from flask import Flask, render_template, request, redirect, session
from db import init_db
from auth import register_user, login_user
from services import add_transaction, get_transactions,get_user_counts
from analytics import get_summary
from services import (
    add_transaction,
    get_transactions,
    get_user_counts,
    get_category_expense,
    get_monthly_data,
    get_income,
    get_expense,
    search_transactions
)
from datetime import datetime

from services import insert_dummy_data
insert_dummy_data()

app = Flask(__name__)
app.secret_key = "secret123"

init_db()

@app.route("/")
def home():
    return redirect("/login")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    admin, analyst, viewer = get_user_counts()

    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]
        role = request.form["role"]

        if register_user(user, pwd, role):
            return redirect("/login")
        else:
            message = "User already exists"

    return render_template("register.html",
                           message=message,
                           admin=admin,
                           analyst=analyst,
                           viewer=viewer)

# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    admin, analyst, viewer = get_user_counts()

    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        role = login_user(user, pwd)

        if role:
            session["role"] = role
            return redirect("/dashboard")
        else:
            message = "Invalid username or password"

    return render_template("login.html",
                           message=message,
                           admin=admin,
                           analyst=analyst,
                           viewer=viewer)

# DASHBOARD
from datetime import datetime

@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "role" not in session:
        return redirect("/login")

    role = session["role"]

    # 📅 GET MONTH (ONLY ONCE)
    selected_month = request.args.get("month")

    if not selected_month:
        selected_month = datetime.now().strftime("%Y-%m")

    # ✅ GET DATA (ONLY ONCE)
    dates, monthly_amounts = get_monthly_data(selected_month)

    # 💰 SUMMARY
    income = get_income()
    expense = get_expense()
    balance = income - expense

    # 📋 TRANSACTIONS
    transactions = get_transactions()

    # 🔍 SEARCH
    search_query = request.args.get("search")
    if search_query:
        transactions = search_transactions(search_query)

    # 📊 CATEGORY
    categories, amounts = get_category_expense()

    # ✅ SAFETY (OPTIONAL)
    dates = dates or []
    monthly_amounts = monthly_amounts or []
    categories = categories or []
    amounts = amounts or []

    return render_template(
        "dashboard.html",
        income=income,
        expense=expense,
        balance=balance,
        transactions=transactions,
        role=role,
        categories=categories,
        amounts=amounts,
        dates=dates,
        monthly_amounts=monthly_amounts,
        selected_month=selected_month
    )

#Update 
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    if session.get("role") != "admin":
        return redirect("/dashboard")

    from services import get_transaction_by_id, update_transaction

    if request.method == "POST":
        update_transaction(
            id,
            request.form["type"],
            float(request.form["amount"]),
            request.form["category"],
            request.form["date"]
        )
        return redirect("/dashboard")

    transaction = get_transaction_by_id(id)
    return render_template("update.html", transaction=transaction)

#Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

#Analytics
@app.route("/analytics")
def analytics_dashboard():
    if session.get("role") not in ["admin", "analyst"]:
        return redirect("/dashboard")

    # Summary
    income = get_income()
    expense = get_expense()
    balance = income - expense

    # Charts Data
    categories, amounts = get_category_expense()
    dates, monthly_amounts = get_monthly_data()

    # Table Data
    transactions = get_transactions()

    return render_template(
        "analytics.html",
        income=income,
        expense=expense,
        balance=balance,
        categories=categories,
        amounts=amounts,
        dates=dates,
        monthly_amounts=monthly_amounts,
        transactions=transactions
    )
#Delete
@app.route("/delete/<int:id>")
def delete(id):
    if session.get("role") != "admin":
        return redirect("/dashboard")

    from services import delete_transaction
    delete_transaction(id)

    return redirect("/dashboard")

#Add
@app.route("/add", methods=["GET", "POST"])
def add():
    if session.get("role") not in ["admin", "analyst"]:
        return redirect("/dashboard")

    if request.method == "POST":
        type_ = request.form["type"]
        amount = float(request.form["amount"])
        category = request.form["category"]
        date = request.form["date"]

        add_transaction(type_, amount, category, date)

        return redirect("/dashboard")

    # return render_template("dashboard.html")
app.run(debug=True)