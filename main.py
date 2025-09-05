from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Create OpenAI client (new API style)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("DEBUG: API key loaded?", bool(os.getenv("OPENAI_API_KEY")))

@app.route('/api/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_input = data.get('question') if data else None

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        modified_prompt = (
            f"You are a helpful assistant providing feedback.\n"
            f"Student input: \"{user_input}\"\n"
            f"Please respond clearly and concisely."
        )

        # Call GPT API only when user sends input
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a writing tutor."},
                {"role": "user", "content": modified_prompt}
            ],
            max_tokens=150
        )

        answer = response.choices[0].message.content.strip()
        return jsonify({"answer": answer})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
