from flask import Flask, render_template, request
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode
import csv

# Database configuration
db_config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'database': 'clear_room'
}

# Initialize the Flask app
app = Flask(__name__)


# Define a route for the home page
@app.route('/')
def loginpage():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/confirm', methods=['POST'])
def confirm():
  return render_template('confirmation.html')


# Define a route for the login page
@app.route('/login',methods=['POST','GET'])
def login():
    password = request.form['password']

    # read the data from the CSV file
    with open('data.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if row['password'] == password:
                # if the email and password are correct, display the home page with a welcome message
                    return render_template('home.html', welcome_message=f"Welcome {row['ï»¿first name']}!")
   
        else:
	         return render_template('login.html', info='Invalid User')
        
@app.route('/log out')
def logout():
    return render_template('login.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


# Define the path to the CSV file
CSV_FILE = 'bookings.csv'

# Define a function to write the bookings data to the CSV file
def write_to_csv(data):
    print("Writing to CSV:", data)
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Define a route to handle the bookings page
@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    print("Inside bookings function")  # Add this line
    if request.method == 'POST':
        room_type = request.form['room-type']
        check_in_date = request.form['check-in-date']
        check_in_time = request.form['check-in-time']
        check_out_time = request.form['check-out-time']
        num_guests = request.form['num-guests']
        
        booking_data = [room_type, check_in_date, check_in_time, check_out_time, num_guests]
        
        # Write the booking data to the CSV file
        write_to_csv(booking_data)
        
        
        return render_template('confirmation.html')
    
    # If the request method is GET, render the bookings.html template
    return render_template('bookings.html')



# Run the Flask app
if __name__ == '__main__':
    app.run()
