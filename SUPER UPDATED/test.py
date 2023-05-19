from flask import Flask, render_template, request
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode
import csv


app = Flask(__name__)


# Define a route for the home page
@app.route('/')
def loginpage():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

#@app.route('/confirm', methods=['POST'])
#def confirm():
  # bookings = get_bookings()
  # return render_template('confirmation.html')

@app.route('/confirm', methods=['POST'])
def confirm():
  return render_template('confirmation.html')


# Define a route for the login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    password = request.form['password']

    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Saramol@2002',
        database='new_schema'
    )

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Execute the SQL query to check the credentials
    query = "SELECT * FROM userdata WHERE Passwords = %s"
    values = (password,)
    cursor.execute(query, values)

    rows = cursor.fetchall()

    if len(rows) > 0:
        # If there are matching rows, display the home page with a welcome message for each row
        welcome_messages = [f"Welcome {row[0]}!" for row in rows]
        return render_template('home.html', welcome_messages=welcome_messages)

    # Close the cursor and database connection
    cursor.close()
    connection.close()

    # If no matching rows are found, display the login page with an error message
    return render_template('login.html', info='Invalid User')
        
@app.route('/log out')
def logout():
    return render_template('login.html')



# Define the path to the feedback CSV file
FEEDBACK_CSV_FILE = 'feedback.csv'

def write_feedback_to_csv(data):
    print("Writing to CSV:", data)
    with open(FEEDBACK_CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Define a route to handle the feedback submission
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    print("Inside feedback function")  # Add this line
    if request.method == 'POST':
        full_name = request.form['full-name']
        email = request.form['email']
        room = request.form['room-number']
        rate = request.form['rate']
        suggestions = request.form['suggestions']
        
        feedback_data = [full_name, email, room, rate, suggestions]
        
        # Write the feedback data to the feedback CSV file
        write_feedback_to_csv(feedback_data)
        
        # You can customize the response or redirect to a thank you page
        return render_template('feedbackreceived.html')
    
    # If the request method is GET, render the bookings.html template
    return render_template('feedback.html')


# Define the path to the CSV file
BOOKINGS_CSV_FILE = 'bookings.csv'

# Define a function to write the bookings data to the CSV file
def write_booking_to_csv(data):
    print("Writing to CSV:", data)
    with open(BOOKINGS_CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Define a route to handle the bookings page
@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    
    if request.method == 'POST':
        room_type = request.form['room-type']
        room_number = request.form['room-number']
        check_in_date = request.form['check-in-date']
        check_in_time = request.form['check-in-time']
        check_out_time = request.form['check-out-time']
        num_guests = request.form['num-guests']

        # Convert check-in and check-out times to datetime objects
        check_in_datetime = datetime.strptime(check_in_date + ' ' + check_in_time, '%Y-%m-%d %H:%M')
        check_out_datetime = datetime.strptime(check_in_date + ' ' + check_out_time, '%Y-%m-%d %H:%M')

        # Check if check-out time is after check-in time
        if check_out_datetime > check_in_datetime:

        # Check room availability
          if is_room_available(room_number,num_guests):
            # Room is available, proceed with the booking
            booking_data = [room_type, room_number, check_in_date, check_in_time, check_out_time, num_guests]
            write_booking_to_csv(booking_data)
            return render_template('confirmation.html')
          else:
            # Room is not available, display an error message
            error_message = 'The selected room is not available or does not have sufficient capacity.'
            return render_template('bookings.html', error_message=error_message)
       
        else:
            # Check-out time is before or equal to check-in time, display an error message
            error_message = 'Invalid check-out time. The check-out time must be after the check-in time.'
            return render_template('bookings.html', error_message=error_message)
    
     # If the request method is GET, render the bookings.html template
    return render_template('bookings.html')


def is_room_available(room_number,num_guests):
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Saramol@2002',
        database='new_schema'
    )

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Execute the SQL query to check room availability
    query = "SELECT Availability, Capacity FROM room_availability WHERE Number = %s"
    values = (room_number,)
    cursor.execute(query, values)

    row = cursor.fetchone()

    # Close the cursor and database connection
    cursor.close()
    connection.close()

    if row is not None and row[0] == 'Yes' and int(num_guests) <= row[1]:
        # Room is available
        return True
    else:
        # Room is not available or does not exist
        return False
        
 


if __name__ == '__main__':
    app.run()
