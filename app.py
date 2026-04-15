#!/usr/bin/env python3
"""
NSFW Content Filter — Flask web app.

Run:
    python app.py
Then open http://localhost:5000
"""

import base64
import json
import os

import anthropic
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB limit

ALLOWED_MIME = {"image/jpeg", "image/png", "image/gif", "image/webp"}

SYSTEM_PROMPT = """You are a content moderation specialist. Analyze the provided image and determine if it contains NSFW (Not Safe For Work) content.

NSFW content includes:
- Explicit nudity or sexual content
- Graphic violence or gore
- Disturbing or shocking imagery

Respond with only a valid JSON object with exactly these fields:
{
  "safe": <true if image is safe/appropriate, false if NSFW>,
  "confidence": <float between 0.0 and 1.0 indicating confidence in the classification>,
  "categories": <list of detected NSFW categories, empty list if safe>,
  "reason": "<one sentence explaining the classification>"
}"""


def classify_image(image_data: bytes, mime_type: str) -> dict:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not configured on the server.")

    client = anthropic.Anthropic(api_key=api_key)
    b64 = base64.standard_b64encode(image_data).decode("utf-8")

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=256,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": mime_type, "data": b64},
                    },
                    {"type": "text", "text": "Classify this image for NSFW content."},
                ],
            }
        ],
    )

    text = next((b.text for b in response.content if b.type == "text"), "")
    return json.loads(text)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename."}), 400

    mime_type = file.mimetype
    if mime_type not in ALLOWED_MIME:
        return jsonify({"error": f"Unsupported file type: {mime_type}"}), 400

    image_data = file.read()

    try:
        result = classify_image(image_data, mime_type)
        threshold = float(request.form.get("threshold", 0.7))
        flagged = not result.get("safe", True) and result.get("confidence", 0) >= threshold
        result["flagged"] = flagged
        return jsonify(result)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse model response."}), 500
    except anthropic.APIError as e:
        return jsonify({"error": f"API error: {e}"}), 502
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
