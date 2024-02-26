from flask import Flask, request, render_template 
import pickle 
import math
 
model = pickle.load (open ('Model/model.pkl', 'rb')) 
 
app = Flask (__name__) 
 
 
@app.route ('/') 
def index (): 
    return render_template ("index.html") 
 
 
@app.route ('/predict', methods =['POST']) 
def predict_result (): 
    
    city_names = { '0': 'Avon and Somerset', '1': 'Bedfordshire', '2': 'Cambridgeshire', '3': 'Cheshire', '4': 'Cleveland'}
    
    crimes_names = { '0': 'Criminal damage and arson', '1': 'Drug offences', '2': 'Fraud offences'}
    
    population = { '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10}
    
    city_code = request.form["city"] 
    crime_code = request.form['crime'] 
    year = request.form['year'] 
    pop = population[city_code] 

    # Here increasing / decreasing the population as per the year.
    # Assuming that the population growth rate is 1% per year.
    year_diff = int(year) - 2011;
    pop = pop + 0.01*year_diff*pop

    
    crime_rate = model.predict ([[year, city_code, pop, crime_code]])[0] 
    
    city_name = city_names[city_code] 
    
    crime_type =  crimes_names[crime_code] 
    
    if crime_rate <= 1:
        crime_status = "Very Low Crime Area" 
    elif crime_rate <= 5:
        crime_status = "Low Crime Area"
    elif crime_rate <= 15:
        crime_status = "High Crime Area"
    else:
        crime_status = "Very High Crime Area" 
    
    cases = math.ceil(crime_rate * pop)
    
    return render_template('result.html', city_name=city_name, crime_type=crime_type, year=year, crime_status=crime_status, crime_rate=crime_rate, cases=cases, population=pop)

if __name__ == '__main__':
    # app.run (debug = False, host='0.0.0.0', port=5000) 
    app.run(debug = False)
