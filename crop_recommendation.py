from flask import Flask, request, jsonify,render_template
import os
import google.generativeai as genai
import json

genai.configure(api_key="AIzaSyDdIimoQuikBlidQlPLScVPH3x2UTfbCHM")

app = Flask(__name__)

# Function to load Google Gemini Pro Vision API And get response
def get_gemini_repsonse(input_prompt, input_data):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input_prompt, input_data])
    return response.text

@app.route('/')
def index():
    return render_template("indexCrop.html")
    # return """
    # <h1>Crop Recommendation System</h1>
    # <form action="/find_crops" method="post">
    #     <label for="nitrogen">Nitrogen:</label>
    #     <input type="text" id="nitrogen" name="nitrogen"><br><br>
    #     <label for="phosphorous">Phosphorous:</label>
    #     <input type="text" id="phosphorous" name="phosphorous"><br><br>
    #     <label for="potassium">Potassium:</label>
    #     <input type="text" id="potassium" name="potassium"><br><br>
    #     <label for="temperature">Temperature:</label>
    #     <input type="text" id="temperature" name="temperature"><br><br>
    #     <label for="humidity">Humidity:</label>
    #     <input type="text" id="humidity" name="humidity"><br><br>
    #     <label for="ph">PH:</label>
    #     <input type="text" id="ph" name="ph"><br><br>
    #     <label for="rainfall">Rainfall:</label>
    #     <input type="text" id="rainfall" name="rainfall"><br><br>
    #     <button type="submit">Find the crops suitable</button>
    # </form>
    # """

@app.route('/find_crops', methods=['POST'])
def find_crops():
    input_nitrogen = request.form['nitrogen']
    input_phosphorous = request.form['phosphorous']
    input_potassium = request.form['potassium']
    input_temperature = request.form['temperature']
    input_humidity = request.form['humidity']
    input_ph = request.form['ph']
    input_rainfall = request.form['rainfall']
    # input_data = input_nitrogen, input_phosphorous, input_potassium, input_temperature, input_humidity, input_ph, input_rainfall
    input_data = {
        'input_ph': input_ph,
        'input_humidity': input_humidity,
        'input_temperature': input_temperature,
        'input_phosphorous': input_phosphorous,
        'input_potassium': input_potassium,
        'input_rainfall': input_rainfall,
        'input_nitrogen': input_nitrogen
    }
    json_data = json.dumps(input_data)
    input_prompt = """
    you are a expert in telling which crop can be grown in which type of place 
    the data given to you will be
    1) Nitrogen
    2) Phosphorous
    3) Potassium
    4) Temperature
    5) Humidity
    6) PH
    7) Rainfall

    you have to give the list of crop that can give a good harvest according to the given info  and provide only the crop names

    give 6 crop and rank them accordingly 
    """
    response = get_gemini_repsonse(input_prompt, json_data)
    return render_template("resultCrop.html", response=response)

if __name__ == '__main__':
    app.run(debug=True)
