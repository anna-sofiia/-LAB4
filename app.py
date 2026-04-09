from flask import Flask, render_template, request
from gtts import gTTS
import os

app = Flask(__name__)

# Папка для збереження згенерованого аудіо
OUTPUT_FOLDER = "static"
OUTPUT_FILE = "output.mp3"


@app.route("/", methods=["GET", "POST"])
def index():
    audio_ready = False
    entered_text = ""
    selected_lang = "uk"

    if request.method == "POST":
        entered_text = request.form.get("text", "").strip()
        selected_lang = request.form.get("language", "uk")

        if entered_text:
            try:
                tts = gTTS(text=entered_text, lang=selected_lang)
                output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
                tts.save(output_path)
                audio_ready = True
            except Exception as e:
                return render_template(
                    "index.html",
                    error=f"Помилка під час генерації мовлення: {e}",
                    text=entered_text,
                    language=selected_lang,
                    audio_ready=False
                )
        else:
            return render_template(
                "index.html",
                error="Будь ласка, введіть текст.",
                text=entered_text,
                language=selected_lang,
                audio_ready=False
            )

    return render_template(
        "index.html",
        audio_ready=audio_ready,
        text=entered_text,
        language=selected_lang
    )


if __name__ == "__main__":
    app.run(debug=True)