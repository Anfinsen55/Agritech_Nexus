import os
import google.generativeai as genai
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_url_path='/static')

# load_dotenv()
genai.configure(api_key="AIzaSyDdIimoQuikBlidQlPLScVPH3x2UTfbCHM")

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        image_parts = [
            {
                "mime_type": uploaded_file.content_type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_prompt = """
        Your task is to analyze images of plant diseases, tell the name of the disease, determine whether they are deadly or common, and provide recommendations for curing them. When presented with an image of a plant disease, describe the symptoms, ascertain the severity, and suggest the appropriate treatment or management approach. Offer insights on preventive measures or interventions that can help control the spread of the disease and ensure plant health.
For instance, when examining an image of a tomato plant with discolored and wilting leaves, you would identify this as a common disease known as Early Blight caused by fungi. You would recommend removing infected plant parts, using fungicides, mulching, and practicing crop rotation to manage the disease effectively. Provide clear, concise explanations and actionable steps for each identified plant disease to help individuals address and prevent further outbreaks through your expertise as a seasoned farmer.
        """

        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        image_data = input_image_setup(file)
        response = get_gemini_response(input_prompt, image_data)
        return render_template("resultDisease.html", response=response)

    return render_template("indexDisease.html")

if __name__ == "__main__":
    app.run(debug=True)