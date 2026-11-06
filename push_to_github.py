#!/usr/bin/env python3
"""
Push files to a GitHub repository using the GitHub REST API.

Requirements:
    pip install requests

Usage:
    export GITHUB_TOKEN=your_personal_access_token
    python push_to_github.py

The script will:
  1. Create or update files in the target repository.
  2. Commit them in a single push.

Note: You need a personal access token with 'repo' scope.
Generate one at: https://github.com/settings/tokens
"""

import os
import base64
import requests

# Configuration - change these as needed
OWNER = "xudaniel"
REPO = "github-derive-tool"
BRANCH = "main"
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise SystemExit("Please set GITHUB_TOKEN environment variable.")

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def get_file_sha(path: str) -> str | None:
    """Get the current SHA of a file if it exists (needed for updates)."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}"
    resp = requests.get(url, headers=HEADERS, params={"ref": BRANCH})
    if resp.status_code == 200:
        return resp.json().get("sha")
    return None


def push_file(path: str, content: str, message: str):
    """Create or update a single file."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}"
    sha = get_file_sha(path)

    payload = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "branch": BRANCH,
    }
    if sha:
        payload["sha"] = sha

    resp = requests.put(url, headers=HEADERS, json=payload)
    if resp.status_code in (200, 201):
        print(f"Successfully pushed: {path}")
        return True
    else:
        print(f"Failed to push {path}: {resp.status_code} {resp.text}")
        return False


def main():
    # Example: push a simple README update and a new file
    example_content = """# Example File

This file was pushed by the push_to_github.py script.
"""

    success = push_file(
        path="example_pushed.txt",
        content=example_content,
        message="Add example file via API push script",
    )

    if success:
        print("\nPush completed. Check the repository:")
        print(f"https://github.com/{OWNER}/{REPO}")
    else:
        print("\nPush failed. Check your token permissions and network.")


if __name__ == "__main__":
    main()
