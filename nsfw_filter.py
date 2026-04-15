#!/usr/bin/env python3
"""
NSFW content filter using Claude's vision capabilities.

Analyzes images and classifies them as safe or unsafe (NSFW).

Usage:
    python nsfw_filter.py image.jpg
    python nsfw_filter.py image1.png image2.jpg --threshold 0.8
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

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


def encode_image(image_path: Path) -> tuple[str, str]:
    """Read and base64-encode an image file. Returns (base64_data, media_type)."""
    ext = image_path.suffix.lower()
    media_type_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    media_type = media_type_map.get(ext, "image/jpeg")
    with open(image_path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    return data, media_type


def classify_image(client: anthropic.Anthropic, image_path: Path) -> dict:
    """Send image to Claude and return NSFW classification result."""
    image_data, media_type = encode_image(image_path)

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
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Classify this image for NSFW content.",
                    },
                ],
            }
        ],
    )

    text = next(
        (block.text for block in response.content if block.type == "text"), ""
    )
    return json.loads(text)


def filter_images(image_paths: list[Path], threshold: float) -> list[dict]:
    """Classify a list of images and return results."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("[ERROR] ANTHROPIC_API_KEY not set in environment.", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    results = []

    for i, path in enumerate(image_paths, 1):
        print(f"  [{i}/{len(image_paths)}] Checking: {path.name} ...", end=" ", flush=True)

        if not path.exists():
            print("NOT FOUND")
            results.append({"file": str(path), "error": "File not found"})
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            print("SKIPPED (unsupported format)")
            results.append({"file": str(path), "error": "Unsupported file format"})
            continue

        try:
            classification = classify_image(client, path)
            safe = classification.get("safe", True)
            confidence = classification.get("confidence", 0.0)
            categories = classification.get("categories", [])
            reason = classification.get("reason", "")

            # Apply threshold: treat as NSFW only if confidence exceeds threshold
            flagged = not safe and confidence >= threshold

            status = "SAFE" if not flagged else "NSFW"
            cats = ", ".join(categories) if categories else "none"
            print(f"{status}  confidence={confidence:.2f}  categories=[{cats}]")
            if reason:
                print(f"      {reason}")

            results.append({
                "file": str(path),
                "safe": not flagged,
                "confidence": confidence,
                "categories": categories,
                "reason": reason,
                "flagged": flagged,
            })
        except (json.JSONDecodeError, anthropic.APIError) as e:
            print(f"ERROR: {e}")
            results.append({"file": str(path), "error": str(e)})

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="NSFW content filter powered by Claude vision."
    )
    parser.add_argument(
        "images",
        nargs="+",
        metavar="IMAGE",
        help="Image file(s) to classify.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        metavar="T",
        help="Confidence threshold to flag content as NSFW (default: 0.7).",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Write results as JSON to this file.",
    )
    args = parser.parse_args()

    image_paths = [Path(p) for p in args.images]
    print(f"Scanning {len(image_paths)} image(s) with threshold={args.threshold}\n")

    results = filter_images(image_paths, threshold=args.threshold)

    flagged = [r for r in results if r.get("flagged")]
    safe = [r for r in results if not r.get("flagged") and "error" not in r]
    errors = [r for r in results if "error" in r]

    print(f"\nSummary: {len(safe)} safe, {len(flagged)} NSFW, {len(errors)} error(s).")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Results written to: {args.output}")

    # Exit with non-zero code if any NSFW content was found
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()
