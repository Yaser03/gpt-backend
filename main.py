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
                        "Provide formative feedback primarily by highlighting their linguistic choices and asking high-quality questions to raise their metacognative awareness. "
                        "Move from high-level conceptual issues to local language features. "
                        "Do not rewrite the student's text.\n\n"
                        "Focus specifically on features that reveal the student's attitude or position toward the original article or author such as:\n"
                        "- Claims and evaluations\n"
                        "- Use of hedging or certainty\n"
                        "- Choice of reporting verbs\n"
                        "- Framing of agreement or disagreement\n"
                        "- Degree of critical engagement\n\n"
                        "Encourage reflection about language choices and tone. "
                        "Do not write an essay, instead number you response with numbers and keep them consice."
                        "Use accessible language. Avoid technical terms such as stance or rhetorical features.\n\n"
                        "Do not use asterisks or markdown formatting. Respond in plain text only."
                        "When evaluative language is too strong or non-academic, suggest options to consider."
                        "Respond only in a numbered list format."
                        "A possible structure is:/n"
                        "-Briefly describe what you notice in the student’s writing.\n"
                        "-Then ask one reflective question or provide one suggestion.\n\n"
                        "Do not write an essay."
                        "Do not include conclusions.
                        "Do not summarize the text."
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            max_tokens=1200,
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
