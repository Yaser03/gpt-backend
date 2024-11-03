from flask import Flask, jsonify, request
import openai
import os

app = Flask(__name__)

# Set up OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')

    try:
        # Call OpenAI GPT API with the user's question
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            max_tokens=150
        )
        answer = response.choices[0].text.strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
