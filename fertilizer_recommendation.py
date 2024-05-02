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
    return render_template("indexFertilizer.html")

@app.route('/find_crops', methods=['POST'])
def find_crops():
    input_nitrogen = request.form['nitrogen']
    input_phosphorous = request.form['phosphorous']
    input_potassium = request.form['potassium']
    input_cropType = request.form['cropType']
    input_area = request.form['area']
    # input_ph = request.form['ph']
    # input_rainfall = request.form['rainfall']
    # input_data = input_nitrogen, input_phosphorous, input_potassium, input_temperature, input_humidity, input_ph, input_rainfall
    input_data = {
        'input_nitrogen': input_nitrogen,
        'input_phosphorous': input_phosphorous,
        'input_potassium': input_potassium,
        'input_cropType': input_cropType,
        'input_area': input_area
        # 'input_ph': input_ph,
        # 'input_rainfall': input_rainfall,
    }
    json_data = json.dumps(input_data)
    input_prompt = """
    You're an experienced fertilizer calculator tailored for different types of crops and field sizes. Your job is to help users determine the fertilizer quantities required based on inputs such as the tree name, area of the field in acres, number of trees, and specific nutrient requirements (Nitrogen, Phosphorus, Potassium).
    For the fertilizer calculation, you need the following inputs:
    1. Input1: Nitrogen
    2. Input2: Phosphorus
    3. Input3: Potassium
    4. Input4: Tree/Crop Name (e.g., Rice, Banana, Wheat)
    5. Input5: Area of the Field in Acres
    For example, for a Cotton Farm with 5 Acre land ans soil compostions as N:150, p:52, K:60 , the fertilizer requirements could include:
    - DAP (Diammonium Phosphate) - 229 kg (4 1/2 Bag)
    - MOP (Muriate of Potash) - 202 kg (4 Bag)
    - Urea - 570 kg (11 1/2 Bag)
    Additionally, for a specific NPK fertilizer blend, the requirement may be:
    - SSP - 658 kg (13 1/4 Bag)
    - MOP (Muriate of Potash) - 202 kg (4 Bag)
    - Urea - 660 kg (13 1/4 Bag)
    Ensure to calculate the total quantity of each fertilizer component needed based on the inputs provided and offer a comprehensive recommendation to meet the optimal nutrient requirements for the specified tree type and field conditions.
    - Fertilizer requirements can vary based on the crop type, soil conditions, and other factors. Professional advice from agricultural experts is recommended for accurate recommendations.
    - Use a fertilizer calculator relevant to your location for precise results.
    - Follow the instructions on fertilizer labels meticulously to avoid environmental harm.
    - Give response in Kg and total and not per acre.
    - Do not add any ** in between the response
    For instance, if the user provides inputs for banana trees with a quantity of 50, the calculator might suggest a combination including DAP, MOP, and Urea in specific quantities, as illustrated in the example provided.
    """
    response = get_gemini_repsonse(input_prompt, json_data)
    return render_template("resultFertilizer.html", response=response)

if __name__ == '__main__':
    app.run(debug=True)
