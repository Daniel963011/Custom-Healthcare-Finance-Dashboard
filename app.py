from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
from database_config import db_connection
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def dashboard():
    connection = db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('dasboard.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        department = request.form['department']
        category = request.form['category']
        amount = request.form['amount']
        description = request.form['description']
        date = request.form['date']

        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO expenses (department, category, amount, description, date)
            VALUES (%s, %s, %s, %s, %s)
        """, (department, category, amount, description, date))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect('/')
    return render_template('add_entry.html')

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_entry(id):
    connection = db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        cursor.execute("DELETE FROM expenses WHERE id = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect('/')

    # GET request: show confirmation page
    cursor.execute("SELECT * FROM expenses WHERE id = %s", (id,))
    expense = cursor.fetchone()
    cursor.close()
    connection.close()

    if not expense:
        return "Expense not found", 404

    return render_template('delete_entry.html', expense=expense)


def export_data():
    connection = db_connection()
    file = pd.read_sql("SELECT * FROM expenses", connection)
    connection.close()

    output = BytesIO()
    file.to_csv(output, index=False)
    output.seek(0)

    return send_file(output, download_name="healthcare_expenses.csv", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
