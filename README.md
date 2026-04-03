# 💰 Finance Dashboard (Flask + SQLite)

A role-based Financial Dashboard System built using **Flask**,and  **SQLite**.

This project allows users to manage transactions, visualize analytics, and track financial data efficiently.

---

## 🚀 Features

### 🔐 Authentication
- User Registration & Login
- Password hashing (Werkzeug)
- Role-based access:
  - Admin
  - Analyst
  - Viewer

---

### 💳 Transaction Management
- Add Transaction
- Update Transaction (Admin only)
- Delete Transaction (Admin only)
- Search Transactions

---

### 📊 Dashboard
- Total Income
- Total Expense
- Balance Calculation
- Transaction Table

---

### 📈 Analytics (Admin & Analyst)
- 📅 Monthly Filter
- 📈 Line Chart (Growth Over Time)
- 📊 Bar Chart (Category Expenses)
- 🥧 Pie Chart (Expense Distribution)
- 📋 Data Table

---

## 🛠️ Tech Stack

- Backend: Flask (Python)
- Database: SQLite
- Frontend: HTML, CSS

---

## 📁 Project Structure


Finance_Dashboard/
│
├── app.py # Main Flask app (routes)
├── db.py # Database connection
├── auth.py # Login & Register logic
├── services.py # DB operations (CRUD)
├── analytics.py # Summary functions (optional)
│
├── templates/
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── analytics.html
│ ├── update.html
│
├── static/ # (optional)
│ ├── style.css
│
└── README.md


---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash```
git clone https://github.com/your-username/finance-dashboard.git
cd finance-dashboard

### 2️⃣ Install Dependencies
pip install flask werkzeug

### 3️⃣ Run Application
python app.py

### 4️⃣ Open in Browser
http://127.0.0.1:5000

🧪 Default Roles
Role	Access
Admin	Full access (CRUD + Analytics)
Analyst	View + Analytics
Viewer	View only

📌 Important Notes
Date format must be: YYYY-MM-DD
SQLite uses ? placeholder (not %s)
Restart server after code changes

🔥 Future Improvements
Export to PDF
Export to Excel
Dark/Light Mode Toggle
User Profile System
JWT Authentication

👨‍💻 Author
Sakshi Bisht
