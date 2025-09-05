from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins (you can restrict later)

# Load OpenAI API key from Render environment
openai.api_key = os.getenv("OPENAI_API_KEY")
print("DEBUG: API key loaded?", bool(openai.api_key))  # Check if API key is detected

@app.route('/api/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        print("DEBUG: Received data:", data)

        user_input = data.get('question') if data else None
        print("DEBUG: Extracted user input:", user_input)

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        # Modify the prompt before sending to GPT
        modified_prompt = (
            f"You are a helpful assistant providing feedback.\n"
            f"Student input: \"{user_input}\"\n"
            f"Please respond clearly and concisely."
        )
        print("DEBUG: Prompt being sent to GPT:", modified_prompt)

        # Call GPT API with the modified prompt
        response = openai.Completion.create(
            model="text-davinci-003",  # ✅ make sure model is correct
            prompt=modified_prompt,
            max_tokens=150
        )

        answer = response.choices[0].text.strip()
        print("DEBUG: GPT Answer:", answer)

        return jsonify({"answer": answer})

    except Exception as e:
        print("ERROR: Exception occurred:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
