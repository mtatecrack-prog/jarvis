from flask import Flask, request, jsonify, send_file
import ollama
import speech_recognition as sr
import subprocess

app = Flask(__name__)

@app.route("/")
def inicio():
    return send_file(r"C:\Jarvis\index.html")

@app.route("/audio", methods=["POST"])
def audio():
    try:
        archivo = request.files["audio"]

        webm = r"C:\Jarvis\voz.webm"
        wav = r"C:\Jarvis\voz.wav"

        archivo.save(webm)

        subprocess.run([
            r"C:\Users\Usuario\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Shared_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build-shared\bin\ffmpeg.exe", "-y",
            "-i", webm,
            "-ar", "16000",
            "-ac", "1",
            wav
        ], capture_output=True)

        reconocedor = sr.Recognizer()

        with sr.AudioFile(wav) as fuente:
            audio = reconocedor.record(fuente)

        texto = reconocedor.recognize_google(
            audio,
            language="es-AR"
        )

        print("[CELULAR]", texto)

        respuesta = ollama.chat(
            model="qwen3:1.7b",
            messages=[
                {
                    "role": "system",
                    "content": "Eres JARVIS, un asistente en español argentino. Responde de forma natural, breve y útil."
                },
                {
                    "role": "user",
                    "content": texto
                }
            ],
            think=False,
            options={"num_predict": 120}
        )

        resultado = respuesta["message"]["content"].strip()

        print("[JARVIS]", resultado)

        return jsonify({
            "texto": texto,
            "respuesta": resultado
        })

    except sr.UnknownValueError:
        return jsonify({
            "texto": "",
            "respuesta": "No pude entender lo que dijiste."
        })

    except Exception as e:
        print("[ERROR]", e)
        return jsonify({
            "texto": "",
            "respuesta": "Ocurrió un error al procesar el audio."
        }), 500

app.run(
    host="0.0.0.0",
    port=5000,
    ssl_context=(
        r"C:\Jarvis\10.93.205.118+2.pem",
        r"C:\Jarvis\10.93.205.118+2-key.pem"
    )
)

