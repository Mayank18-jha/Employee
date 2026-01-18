import sqlite3
import os

DB_DIR = "database"
DB_PATH = os.path.join(DB_DIR, "company.db")
os.makedirs(DB_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    salary INTEGER,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(id)
)
""")

conn.commit()

def add_department():
    name = input("Department name: ")
    cursor.execute("INSERT OR IGNORE INTO departments (name) VALUES (?)", (name,))
    conn.commit()
    print("✅ Department added")

def add_employee():
    name = input("Employee name: ")
    age = int(input("Age: "))
    salary = int(input("Salary: "))
    dept_id = int(input("Department ID: "))

    cursor.execute("""
    INSERT INTO employees (name, age, salary, department_id)
    VALUES (?, ?, ?, ?)
    """, (name, age, salary, dept_id))
    conn.commit()
    print("✅ Employee added")

def view_employees():
    cursor.execute("""
    SELECT e.id, e.name, e.age, e.salary, d.name
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    """)
    rows = cursor.fetchall()

    print("\nID | Name | Age | Salary | Department")
    print("-" * 50)
    for row in rows:
        print(row)

def department_salary_report():
    cursor.execute("""
    SELECT d.name, COUNT(e.id), AVG(e.salary)
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    GROUP BY d.name
    """)
    rows = cursor.fetchall()

    print("\nDepartment | Employees | Avg Salary")
    print("-" * 50)
    for row in rows:
        print(row)

def menu():
    while True:
        print("""
====== Employee Management System ======
1. Add Department
2. Add Employee
3. View Employees
4. Department Salary Report
5. Exit
""")
        choice = input("Enter choice: ")

        if choice == "1":
            add_department()
        elif choice == "2":
            add_employee()
        elif choice == "3":
            view_employees()
        elif choice == "4":
            department_salary_report()
        elif choice == "5":
            print("👋 Exiting system")
            break
        else:
            print("❌ Invalid choice")

menu()
conn.close()
