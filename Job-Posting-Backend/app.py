import os
import uuid
from flask import Flask, request, send_file, jsonify
from modules.OpenAIGenerator import OpenAIGenerator
from flask_cors import CORS
import base64
import json

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

      new_filename1 = str(uuid.uuid4()) + '.png'
      image_url1 = image_generator.get_image_url(prompt)
      image_path1 = os.path.join("static/img", new_filename1)
      image_generator.download_image(image_url1, image_path1)

      with open(image_path, "rb") as f:
        image_bytes = f.read()
      image_base64 = base64.b64encode(image_bytes).decode("utf-8")

      with open(image_path1, "rb") as f:
        image_bytes1 = f.read()
      image_base641 = base64.b64encode(image_bytes1).decode("utf-8")

      # Wrap the encoded image data in a dictionary
      response_data = {"image": image_base64, "image1": image_base641}  
      # Enviar la imagen como respuesta
      return jsonify(response_data)

    except Exception as e:
      #Error code: 400 - {'error': {'code': 'content_policy_violation', 'message': 'Your request was rejected as a result of our safety system. Your prompt may contain text that is not allowed by our safety system.', 'param': None, 'type': 'invalid_request_error'}}
      error_message = e.message if hasattr(e, 'message') else str(e)

      if "content_policy_violation" in error_message:
        error_message = "Tu solicitud fue rechazada debido a nuestro sistema de seguridad."
      return jsonify({"error": error_message}), 400
    
# @app.route('/ImageGeneratorExample', methods=['POST'])
# def send_example_image():
#     try:
#         # Read the example image from the static folder
#         with open(os.path.join("static", "img", "im.png"), "rb") as f:
#             image_bytes = f.read()

#         # Encode the image bytes in base64
#         image_base64 = base64.b64encode(image_bytes).decode("utf-8")

#         # Wrap the encoded image data in a dictionary
#         response_data = {"image": image_base64}
        
#         # Send the JSON response
#         return jsonify(response_data)

#     except FileNotFoundError:
#         # Handle the case where the image file is not found
#         return jsonify({"error": "Example image not found"}), 404

#     except Exception as e:
#         # Handle other potential errors
#         print(e)
#         return jsonify({"error": "Error sending example image"}), 500

if __name__ == '_app_':
    app.run(debug=True, port = 5000)
