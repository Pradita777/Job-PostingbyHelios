import os
import uuid
from modules.ImageGenerator import ImageGenerator, ImageGeneratorException
from flask import Flask, request, send_file, jsonify
from modules.OpenAIGenerator import OpenAIGenerator
from flask_cors import CORS
import base64


app = Flask(__name__)
CORS(app)

image_generator = OpenAIGenerator()

@app.route('/ImageGenerator', methods=['POST'])
def generate_image():
  if request.method == 'POST':
    try:
      prompt = request.get_json()['text']
      new_filename = str(uuid.uuid4()) + '.png'
      image_url = image_generator.get_image_url(prompt)
      image_path = os.path.join("static/img", new_filename)
      image_generator.download_image(image_url, image_path)

      with open(image_path, "rb") as f:
        image_bytes = f.read()
      image_base64 = base64.b64encode(image_bytes).decode("utf-8")
      # Wrap the encoded image data in a dictionary
      response_data = {"image": image_base64}  
      image_base64 = base64.b64encode(image_bytes).decode("utf-8")
      # Enviar la imagen como respuesta
      return jsonify(response_data)

    except Exception as e:
      print(e)
      return jsonify({"error": "Error generating image"})
    
@app.route('/ImageGeneratorExample', methods=['POST'])
def send_example_image():
    try:
        # Read the example image from the static folder
        with open(os.path.join("static", "img", "im.png"), "rb") as f:
            image_bytes = f.read()

        # Encode the image bytes in base64
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # Wrap the encoded image data in a dictionary
        response_data = {"image": image_base64}
        
        # Send the JSON response
        return jsonify(response_data)

    except FileNotFoundError:
        # Handle the case where the image file is not found
        return jsonify({"error": "Example image not found"}), 404

    except Exception as e:
        # Handle other potential errors
        print(e)
        return jsonify({"error": "Error sending example image"}), 500

if __name__ == '_app_':
    app.run(debug=True, port = 5000)
