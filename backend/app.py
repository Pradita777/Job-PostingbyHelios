import os
import cv2
import openai
import numpy as np
import base64
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, redirect

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/', methods=('POST','GET'))
def index():
    if request.method == 'POST':
        prompt = request.form['text']
        response = openai.images.generate(
            model='dall-e-3',
            prompt=prompt,
            size='1024x1024',
            quality='standard',
            n=1,
        )

        image_url = response.data[0].url
        image_data = requests.get(image_url).content
        static_folder = "static"
        image_path = os.path.join(static_folder, "siamese_cat.png")

        with open(image_path, "wb") as f:
            f.write(image_data)

        return redirect(url_for("index"))
    return render_template('index.html')

