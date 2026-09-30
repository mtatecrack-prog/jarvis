from flask import Flask, request, jsonify, send_file
from groq import Groq
import os

app = Flask(__name__)

# La API key se obtiene desde las variables de entorno de Render
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def inicio():
    return send_file("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        datos = request.get_json()

        texto = datos.get("texto", "").strip()

        if not texto:
            return jsonify({
                "respuesta": "No recibí ningún mensaje, señor."
            })

        respuesta = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres JARVIS, un asistente personal. "
                        "Hablas español argentino de forma natural. "
                        "Sé breve, claro y útil. "
                        "Al final de tus respuestas llama al usuario 'señor'."
                    )
                },
                {
                    "role": "user",
                    "content": texto
                }
            ],
            temperature=0.7,
            max_tokens=200
        )

        resultado = respuesta.choices[0].message.content.strip()

        return jsonify({
            "texto": texto,
            "respuesta": resultado
        })

    except Exception as e:
        print("[ERROR]", e)

        return jsonify({
            "respuesta": "Ocurrió un error al procesar la orden, señor."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )