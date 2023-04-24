from flask import Flask, request, jsonify
import threading
import nesesi

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form.get('question')
    if user_question:
        response = nesesi.ask_question(user_question)
        return jsonify({"response": response})
    else:
        return jsonify({"error": "No question provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)