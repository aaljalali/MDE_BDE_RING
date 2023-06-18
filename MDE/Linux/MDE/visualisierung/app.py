from flask import Flask, render_template
import random
import sqlite3

app = Flask(__name__)
DATABASE = 'your_database.db'

def create_table():
    # Connect to the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS test (label TEXT, size INTEGER, date TEXT)")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def insert_test_data():
    # Connect to the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Generate random data for the test table
    labels = ['HB', 'An und nicht bekannt', 'An und läuft nicht', 'An und läuft']
    sizes = [20, 10, 30, 40]

    # Insert the test data into the table
    for label, size in zip(labels, sizes):
        cursor.execute("INSERT INTO test (label, size) VALUES (?, ?)", (label, size))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def get_data(time_period):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if time_period == 'last_year':
        cursor.execute("SELECT label, size FROM test WHERE date >= date('now', '-1 year')")
    elif time_period == 'last_month':
        cursor.execute("SELECT label, size FROM test WHERE date >= date('now', '-1 month')")
    elif time_period == 'last_week':
        cursor.execute("SELECT label, size FROM test WHERE date >= date('now', '-7 days')")
    elif time_period == 'last_day':
        cursor.execute("SELECT label, size FROM test WHERE date >= date('now', '-1 day')")
    else:
        cursor.execute("SELECT label, size FROM test")

    data = cursor.fetchall()
    conn.close()

    return data



@app.route('/')
def home():
    # Generate random data for the pie chart
    time_period = 'year'  # Default to the last year
    labels, sizes = zip(*get_data(time_period))
    colors = ['#FF6384', '#36A2EB', '#FFCE56', '#33FF7A']

    return render_template('dashboard.html', labels=labels, sizes=sizes, colors=colors)

if __name__ == '__main__':
    
    create_table()
    #insert_test_data()
    app.run(port=5001)
