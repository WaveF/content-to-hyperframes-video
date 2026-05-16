#!/usr/bin/env python3
"""Generate image via framefly relay's gpt-image-2 model.

Usage:
    python3 generate.py "a cute cat" [--n 1] [--size 1024x1024]

Output:
    Saves PNG to /tmp/framefly-img-<timestamp>.png and prints the path.
"""
import sys
import os
import json
import base64
import time
import argparse
import ssl
from urllib.request import Request, urlopen
from urllib.error import URLError

API_KEY = "KEY_REMOVED"
BASE_URL = "https://relay.framefly.com.cn/v1"
OUTPUT_DIR = "/tmp"


def generate_image(prompt: str, n: int = 1, size: str = "1024x1024") -> str:
    payload = json.dumps({
        "model": "gpt-image-2",
        "prompt": prompt,
        "n": n,
        "size": size,
    }).encode("utf-8")

    ctx = ssl._create_unverified_context()
    req = Request(
        f"{BASE_URL}/images/generations",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        method="POST",
    )

    resp = urlopen(req, timeout=300, context=ctx)
    data = json.loads(resp.read().decode("utf-8"))

    b64 = data["data"][0]["b64_json"]
    img_data = base64.b64decode(b64)

    ts = int(time.time() * 1000)
    out_path = os.path.join(OUTPUT_DIR, f"framefly-img-{ts}.png")
    with open(out_path, "wb") as f:
        f.write(img_data)

    return out_path


def main():
    parser = argparse.ArgumentParser(description="Generate image via framefly gpt-image-2")
    parser.add_argument("prompt", nargs="*", help="Image description")
    parser.add_argument("--n", type=int, default=1, help="Number of images (default: 1)")
    parser.add_argument("--size", default="1024x1024", help="Image size (default: 1024x1024)")
    args = parser.parse_args()

    if not args.prompt:
        prompt = sys.stdin.read().strip()
    else:
        prompt = " ".join(args.prompt)

    if not prompt:
        print("Error: no prompt provided", file=sys.stderr)
        sys.exit(1)

    try:
        out_path = generate_image(prompt, args.n, args.size)
        print(out_path)
    except URLError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
