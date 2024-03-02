from flask import Flask, request, render_template 
import pickle 
import math
 
model = pickle.load(open('Model/model.pkl', 'rb')) 
 
app = Flask(__name__) 

city_names = { '0': 'Avon and Somerset', '1': 'Bedfordshire', '2': 'Cambridgeshire', '3': 'Cheshire', '4': 'Cleveland', '5': 'Cumbria', '6': 'Derbyshire', '7': 'Devon and Cornwall', '8': 'Dorset', '9': 'Durham', '10': 'Dyfed-Powys', '11': 'Essex', '12': 'Gloucestershire', '13': 'Greater Manchester', '14': 'Gwent', '15': 'Hampshire', '16': 'Hertfordshire', '17': 'Humberside', '18': 'Kent'}
crimes_names = { '0': 'Criminal damage and arson', '1': 'Drug offences', '2': 'Miscellaneous crimes against society', '3': 'Possession of weapons', '4': 'Public order offences', '5': 'Robbery', '6': 'Sexual offences', '7': 'Theft offences', '8': 'Violence against the person'}
population = { '0': 1720.00, '1': 665.00, '2': 856.00, '3': 518.50, '4': 557.00, '5': 500.00, '6': 930.00, '7': 1800.00, '8': 774.00, '9': 629.00, '10': 515.00, '11': 1850.00, '12': 637.30, '13': 2700.00, '14': 576.70, '15': 1984.40, '16': 1500.20, '17': 932.80, '18':1800.30}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict_result():
    city_code = request.form.get("city")
    crime_code = request.form.get('crime')
    year = request.form.get('year')

    # Check if all fields are selected
    if not all([city_code, crime_code, year]):
        return render_template('index.html', alert_message="Please select all fields.")

    pop = population[city_code] 

    # Adjusting Population According to the Year.
    # Assuming a 1% Annual Population Growth Rate.
    year_diff = int(year) - 2011;
    pop = pop + 0.01*year_diff*pop
    
    crime_rate = model.predict([[year, city_code, pop, crime_code]])[0] 
    city_name = city_names[city_code] 
    crime_type =  crimes_names[crime_code] 
    
    if crime_rate <= 1:
        crime_status = "Very Low Crime Zone" 
    elif crime_rate <= 5:
        crime_status = "Low Crime Zone"
    elif crime_rate <= 15:
        crime_status = "High Crime Zone"
    else:
        crime_status = "Very High Crime Zone" 
    
    cases = math.ceil(crime_rate * pop)
    
    return render_template('result.html', city_name=city_name, crime_type=crime_type, year=year, crime_status=crime_status, crime_rate=crime_rate, cases=cases, population=pop)

if __name__ == '__main__':
    app.run(debug=False)
