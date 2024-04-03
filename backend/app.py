import os
from flask import Flask, render_template, request, url_for, redirect
from modules.OpenAIGenerator import OpenAIGenerator

app = Flask(__name__)

image_generator = OpenAIGenerator()


@app.route('/', methods=('POST', 'GET'))
def index():
    if request.method == 'POST':
        prompt = request.form['text']
        image_url = image_generator.get_image_url(prompt)
        static_folder = "static"
        image_path = os.path.join(static_folder, "generated_image.png")
        image_generator.download_image(image_url, image_path)
        return redirect(url_for("index"))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
