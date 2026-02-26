import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

def get_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. "
            "Add it to your Render service (Environment → Add Environment Variable)."
        )
    return OpenAI(api_key=api_key)

@app.route('/api/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json(silent=True) or {}
        user_input = data.get("question")

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        client = get_client()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                       "You are a helpful writing tutor. "
                        "Provide formative feedback primarily by asking high-quality, sequenced questions. "
                        "Lead with questions. Move from high-level conceptual issues to local language features. "
                        "Do not rewrite the student's text.\n\n"
                        "Focus specifically on features that reveal the student's attitude or position toward the original article or author such as:\n"
                        "- Claims and evaluations\n"
                        "- Use of hedging or certainty\n"
                        "- Choice of reporting verbs\n"
                        "- Framing of agreement or disagreement\n"
                        "- Degree of critical engagement\n\n"
                        "Encourage reflection about language choices and tone. "
                        "Use accessible language. Avoid technical terms such as stance or rhetorical features.\n\n"
                        "Do not use asterisks or markdown formatting. Respond in plain text only."
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            max_tokens=700,
            temperature=0.7
        )

        answer = (response.choices[0].message.content or "").strip()

        return jsonify({"answer": answer})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Server error: " + str(e)}), 500


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=True
    )
