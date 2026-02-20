import subprocess
import os
import requests
import sys

# 1. Configuration
# Get your key from https://aistudio.google.com/
API_KEY = os.getenv("AI_KEY")
# Using Gemini 2.0 Flash (Fast & Free)
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def get_staged_diff():
    try:
        return subprocess.check_output([
            "git", "diff", "--cached", "--", ":!*.json", ":!*.lock"
        ]).decode("utf-8")
    except Exception:
        return ""

def review_code(diff):
    if not diff:
        return "PASS"

    # --- FIX: Define the prompt BEFORE using it ---
    system_prompt = (
        "You are a strict Senior Developer. Review the git diff below.\n"
        "1. Identify security risks (keys, injections).\n"
        "2. Identify logic bugs or infinite loops.\n"
        "3. Suggest a concise fix.\n"
        "Output a Markdown table. If there are critical errors, end with 'STATUS: REJECT'. "
        "Otherwise, end with 'STATUS: PASS'."
    )

    # Gemini's specific JSON structure
    payload = {
        "contents": [{
            "parts": [{"text": f"{system_prompt}\n\nReview this diff:\n{diff}"}]
        }]
    }

    # Send request (Gemini takes the key as a URL parameter)
    response = requests.post(f"{URL}?key={API_KEY}", json=payload)
    
    if response.status_code != 200:
        print(f"❌ API Error ({response.status_code}): {response.text}")
        sys.exit(1)

    res_json = response.json()
    try:
        return res_json['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError):
        print("❌ Error: Unexpected response format from Gemini.")
        sys.exit(1)

if __name__ == "__main__":
    if not API_KEY:
        print("Error: AI_KEY environment variable not set.")
        sys.exit(1)

    changes = get_staged_diff()
    if not changes:
        print("No staged changes to review.")
        sys.exit(0)

    print(" AI (Gemini) is reviewing your changes...")
    analysis = review_code(changes)
    print("\n" + analysis + "\n")

    if "STATUS: REJECT" in analysis:
        print("❌ [GATEKEEPER] Commit blocked.")
        sys.exit(1)
    else:
        print("✅ [GATEKEEPER] Review passed.")
        sys.exit(0)
