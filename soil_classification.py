import os
import google.generativeai as genai
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_url_path='/static')

# load_dotenv()
genai.configure(api_key="YOUR API KEY")

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
        You're an AI bot with exceptional expertise in soil science and crop cultivation. Your task is to classify the name of the soil from the image provided and suggest five crops that can be successfully planted in that particular type of soil.
Please analyze the soil characteristics shown in the image and identify the type of soil present. Based on this classification, recommend five specific crops that are well-suited for cultivation in this soil type. Be detailed in your analysis and provide reasoning for why each suggested crop thrives in this particular soil.
For example, if the image depicts loamy soil with good drainage and fertility, you could suggest crops like tomatoes, cucumbers, carrots, beans, and bell peppers due to their preference for well-drained, nutrient-rich soils like loam. in 10 lines max.
        """

        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        image_data = input_image_setup(file)
        response = get_gemini_response(input_prompt, image_data)
        return render_template("resultSoil.html", response=response)

    return render_template("indexSoil.html")

if __name__ == "__main__":
    app.run(debug=True)
