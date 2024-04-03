import os
import uuid
from flask import Flask, render_template, request, url_for, redirect
from modules.OpenAIGenerator import OpenAIGenerator
from flask_cors import CORS

app = Flask(__name__)

cors= CORS(app, origins='*')

image_generator = OpenAIGenerator()

image_list = []

def renombrar_imagen(nombre_actual, nuevo_nombre):
    try:
        if os.path.exists(nombre_actual):
            os.rename(nombre_actual, nuevo_nombre)
            print(f"La imagen {nombre_actual} ha sido renombrada a {nuevo_nombre}.")
        else:
            print(f"La imagen {nombre_actual} no existe.")
    except Exception as e:
        print(f"Error al renombrar la imagen: {e}")


@app.route('/', methods=('POST', 'GET'))
def index():
    if request.method == 'POST':
        prompt = request.form['text']
        newFilename = str(uuid.uuid4()) + '.png'
        image_list.append(newFilename)  
        renombrar_imagen("static/img/" + "im.png", "static/img/" + newFilename)
        filename = 'im.png'
        image_url = image_generator.get_image_url(prompt)
        static_folder = "static/img"
        image_path = os.path.join(static_folder, filename)
        image_generator.download_image(image_url, image_path)
        return redirect(url_for("index"))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
