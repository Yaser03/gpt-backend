import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

def get_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        # Clear, friendly error for local/dev logs; Render will show this too.
        raise RuntimeError(
            "OPENAI_API_KEY is not set. "
            "Add it to your Render service (Environment → Add Environment Variable)."
        )
    return OpenAI(api_key=api_key)

@app.route('/api/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json(silent=True) or {}
        user_input = data.get('question')

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

     modified_prompt = (
        "You are a helpful writing tutor, providing formative feedback primarily through highlighting "
        "the features in the students’ text and asking high-quality questions that promote the learner’s "
        "metacognitive awareness and self reflection.\n"
        f"Student input: \"{user_input}\"\n"
        "Please respond clearly and concisely. Do not rewrite their text. Lead with questions.\n"
        "Sequence questions from high-level to local.\n"
        "Focus on features of text that show the student's stance toward the original article or author."
    )

        client = get_client()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",   # modern, low-cost, fast model
            messages=[
                {"role": "system", "content": "You are a writing tutor."},
                {"role": "user", "content": modified_prompt}
            ],
            max_tokens=700,
        )

        answer = (resp.choices[0].message.content or "").strip()
        return jsonify({"answer": answer})

    except Exception as e:
        # Don't leak secrets; just log the message.
        print("ERROR:", str(e))
        return jsonify({"error": "Server error: " + str(e)}), 500

if __name__ == '__main__':
    # On Render, Gunicorn will run this; locally this is fine too.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
