from flask import Flask, render_template, request, jsonify
import json
import os
import openai
from nesesi import load_api_key, transcrever_e_responder, gravar_audio

app = Flask(__name__)
openai.api_key = load_api_key('apikey.txt')

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/send_prompt', methods=['POST'])
def send_prompt():
    user_input = request.form['prompt']
    messages = json.loads(request.form['messages'])
    transcrever_e_responder(messages, user_input)
    return jsonify(messages)

@app.route('/record_audio', methods=['POST'])
def record_audio():
    audio_file = request.files['audio_data']
    audio_file.save('gravacao.wav')

    messages = json.loads(request.form['messages'])

    user_input, response_text = transcrever_e_responder(messages)  # Esta função agora retorna o texto transcrito e a resposta da AI

    os.remove('gravacao.wav')
    return jsonify({"user_input": user_input, "response": response_text})  # Retorne o texto transcrito e a resposta da AI


if __name__ == '__main__':
    app.run(debug=True)

# 