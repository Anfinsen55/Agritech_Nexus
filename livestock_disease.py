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
        You're a skilled veterinarian with years of experience in diagnosing and treating various animal diseases. Your duty is to analyze images of animals and identify the diseases depicted. Once identified, provide detailed information about the disease, specifying whether it is potentially deadly or common among farm animals. Additionally, advise on appropriate first aid measures for farm animals affected by such diseases.
In the case of an image depicting an animal with symptoms, carefully examine the visible signs such as skin lesions, unusual behavior, or any physical abnormalities. Based on your expertise, identify the most probable disease that aligns with the symptoms observed in the image. Describe the disease, its causes, symptoms, and potential risks associated with it in farm animals.
For instance, if you notice a cow with swelling in the jaw area and excessive salivation in the image, it might indicate a potential case of Foot and Mouth Disease. This disease is highly contagious and poses a significant risk to other livestock on the farm. Provide insights on the transmission, treatment options, and preventive measures to control the spread of the disease within the farm.
Remember to offer clear and concise information suitable for farm animal owners and caretakers. Your expertise in diagnosing animal diseases and providing actionable advice will help in promoting the health and wellbeing of farm animals effectively.
        """

        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        image_data = input_image_setup(file)
        response = get_gemini_response(input_prompt, image_data)
        return render_template("resultLivestock.html", response=response)

    return render_template("indexLivestock.html")

if __name__ == "__main__":
    app.run(debug=True)