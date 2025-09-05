from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

# OpenAI API key from Render environment
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get('question')

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # --- MODIFY THE PROMPT HERE ---
    # Example: prepend instructions or context
    modified_prompt = (
        f"You are a helpful assistant providing feedback.\n"
        f"Student input: \"{user_input}\"\n"
        f"Please respond clearly and concisely."
    )

    try:
        # Call GPT API with the modified prompt
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=modified_prompt,
            max_tokens=150
        )
        answer = response.choices[0].text.strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
