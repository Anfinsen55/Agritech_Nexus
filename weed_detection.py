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
        You're an advanced AI system designed to assist in agricultural management, specifically focusing on weed detection in crop fields. Your primary function is to analyze images of fields and accurately identify and locate weeds for efficient removal and crop protection.
        Task:
        Please analyze the provided image of an agricultural field and detect any weeds present. Highlight the areas where weeds are visible and provide recommendations for their removal or treatment.
        Details:
        - Name of the Weed.
        - Analyze the entire image pixel by pixel to identify any anomalies resembling weeds.
        - Categorize the weeds based on their type and density to determine the severity of infestation.
        - Provide precise coordinates or outlines of the weed-infested areas for easy identification and intervention.
        - Suggest appropriate weed management strategies such as manual removal, herbicide application, or other environmentally friendly methods based on the weed type and field conditions.
        Example:
        Given an aerial image of a wheat field, identify the patches of thistle weeds present near the northwest corner. Outline the weed-infested areas and recommend targeted spot treatment to prevent further spread.

        If no weed is present Say No weed present.

        Always answer in English.
        """

        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        image_data = input_image_setup(file)
        response = get_gemini_response(input_prompt, image_data)
        return render_template("resultWeed.html", response=response)

    return render_template("indexWeed.html")

if __name__ == "__main__":
    app.run(debug=True)
