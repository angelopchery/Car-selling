from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['car_parking']
parking_lot = db['parking_lot']

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Parking lot status route
@app.route('/parking-status')
def parking_status():
    status = parking_lot.find()
    return render_template('parking_status.html', status=status)

# Park a car route
@app.route('/park', methods=['POST'])
def park_car():
    if request.method == 'POST':
        car_number = request.form['car_number']
        parking_lot.insert_one({'car_number': car_number})
        return redirect(url_for('parking_status'))

# Remove a car route
@app.route('/remove/<car_number>')
def remove_car(car_number):
    parking_lot.delete_one({'car_number': car_number})
    return redirect(url_for('parking_status'))

if __name__ == '__main__':
    app.run(debug=True)
