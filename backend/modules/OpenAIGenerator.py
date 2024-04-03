from typing import Optional
from openai import OpenAI
import requests
from dotenv import load_dotenv

from modules.ImageGenerator import ImageGenerator
load_dotenv()
client = OpenAI()

s_prompt = """
Eres una IA que se especializa en crear descripciones detalladas y atractivas para imágenes de ofertas de empleo. Tus prompts ayudarán a una IA visual a generar el fondo y los elementos temáticos adecuados que se alineen con una variedad de posiciones laborales.  Recuerda evitar incluir cualquier texto real o logotipos específicos de la empresa en los elementos visuales. Tu trabajo es extender un prompt para la generación de imágenes de vacantes que dijimos antes, de esta manera, obtenemos una imagen lo suficientemente aprovechable para una empresa que quiera utilizar la imagen. 


Para esto, tendrás en cuenta dos elementos; el prompt y el contexto:
<prompt> :: Es la entrada que indica lo que el cliente ha escrito que quiere para la vacante. 
<contexto> :: hace referencia a un tipo de acción al que está orientado el sistema actualmente, pueden ser crear o editar. 

Si es crear, entonces, teniendo en cuenta el prompt inicial, crearás un prompt para la generación de esa imagen, cuidando que la imagen generada cumpla con todos los siguientes puntos.


- Debes dar contexto del objetivo de la imagen. e.g. "Crear una imagen publicitaria de una oferta de empleo que muestre..."

- Descripción de la persona o las personas, que se muestran en la imagen incluyendo sus prendas y facciones. e.g. "...una mujer sonriente con un aspecto profesional y amigable vestida con una blusa blanca y un chaleco rojo, llevando un distintivo con un cordón"

- Detalles sobre el entorno. Debe de describir el ambiente que debe ser plasmado en la imagen. Debe estar orientado al puesto de trabajo. e.g. "El fondo será borroso con una ambientación de oficina o supermercado"

- Especificación del apartado de la información. Debes especificar, la forma, posición y color de la figura que tendrá la información de la vacante. Siempre menciona que este sección debe estar completamente vacía. e.g.

 - Recuerda evitar incluir cualquier texto real o logotipos específicos de la empresa en los elementos visuales.

# Ejemplo de un prompt para el puesto de auxiliar de pago en un supermercado: 

"Crear una imagen publicitaria de una oferta de empleo que muestre a una mujer sonriente con un aspecto profesional y amigable. Debe estar vistiendo una blusa blanca con un chaleco rojo y llevando un distintivo con un cordón. La imagen debe incluir un fondo de oficina o supermercado borroso. En la parte superior debe haber un cuadrado completamente blanco que es el espacio donde irá la información de la vacante. Evita cualquier texto real o logotipos específicos de empresas en la imagen, como si fuera una plantilla vacía."


Por otra parte, si es editar, crearás un prompt corto lo suficientemente específico para llevar a cabo la edición de la imagen.

El prompt estará dentro de los divisores ####. Debes entregar un texto que será el prompt que recibirá el generador de imágenes. No incluyas algo más allá de este texto.

"""


def image_variation(image_name):
    """
        Crea variaciones de una imagen proporcionada utilizando la API de variación de imágenes de OpenAI.

        Parámetros:
        - image_name (str): La ruta al archivo de la imagen para la cual se crearán variaciones.

        Devuelve:
        - str: La URL de la primera variación de imagen generada.

        Ejemplo:
        variation_url = image_variation("ruta/a/la/imagen/original.jpg")
        print(variation_url)  # Imprime la URL de la primera variación de la imagen.
    """
    response = client.images.create_variation(
        image=open(image_name, "rb"),
        n=2,
        size="1024x1024"
    )

    image_url = response.data[0].url
    return image_url


class OpenAIGenerator(ImageGenerator):

    def extend_prompt(self, initial_prompt: str) -> Optional[str]:
        """
           Toma un prompt inicial del usuario y lo envía al modelo GPT-3.5-turbo para generar una versión extendida.

           Parámetros:
           - initial_prompt (str): El prompt inicial proporcionado por el usuario.

           Devuelve:
           - str: El mensaje de texto extendido generado por el modelo.

           Ejemplo:
           extended_prompt = extend_prompt("Escribe un prompt creativo para una oferta de empleo")
           print(extended_prompt)  # Imprime la versión extendida del prompt.
        """
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": s_prompt},
                {"role": "user", "content": "f#### {initial_prompt} ####"}
            ]
        )
        extended_message = completion.choices[0].message.content
        return extended_message

    def get_image_url(self, prompt: str) -> str:
        """
            Genera una imagen basada en un prompt de texto detallado utilizando el modelo DALL-E 3 de OpenAI.

            Parámetros:
            - prompt (str): El prompt de texto detallado que describe la imagen deseada.

            Devuelve:
            - str: La URL de la imagen generada.

            Ejemplo:
            image_url = create_image("Una ilustración de un programador feliz en una oficina moderna")
            print(image_url)  # Imprime la URL de la imagen generada.
        """
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard",
        )

        image_url = response.data[0].url
        return image_url

    def edit_image(self, image_url):
        pass

    def get_image(self, prompt: str) -> str:
        """
        Crea imagenes de vacantes a partir de un prompt detallado utilizando a <extend_prompt> y
        retorna la imagen recibiendola con <create_image>. Guarda la imagen utilizando la función
        <save_image>

        Parámetros:
        - prompt: str con la descripción de la vacante que desea el usuario.
        """
        new_prompt = self.extend_prompt(prompt)
        image_url = self.get_image_url(new_prompt)
        return image_url

    def download_image(self, image_url: str, path: str) -> None:
        image_data = requests.get(image_url).content
        with open(path, "wb") as file:
            file.write(image_data)
