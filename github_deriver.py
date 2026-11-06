#!/usr/bin/env python3
"""
GitHub Deriver - A simple program to derive insights from GitHub users and repositories.

Usage:
    python github_deriver.py <username>

Requires: requests (pip install requests)
Optional: Set GITHUB_TOKEN environment variable for higher rate limits.
"""

import os
import sys
import requests
from collections import Counter
from datetime import datetime

API_BASE = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github.v3+json"}

if token := os.getenv("GITHUB_TOKEN"):
    HEADERS["Authorization"] = f"token {token}"


def get_json(url: str) -> dict | list | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            print("Rate limit exceeded. Set GITHUB_TOKEN for higher limits.")
            return None
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None


def derive_user(username: str):
    user = get_json(f"{API_BASE}/users/{username}")
    if not user:
        print(f"Could not fetch user: {username}")
        return

    print(f"\n=== User: {user.get('login')} ===")
    print(f"Name: {user.get('name') or 'N/A'}")
    print(f"Bio: {user.get('bio') or 'N/A'}")
    print(f"Location: {user.get('location') or 'N/A'}")
    print(f"Public repos: {user.get('public_repos')}")
    print(f"Followers: {user.get('followers')} | Following: {user.get('following')}")
    print(f"Created: {user.get('created_at')}")

    repos = get_json(f"{API_BASE}/users/{username}/repos?sort=stars&per_page=100")
    if not repos:
        return

    # Top 10 by stars
    top = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:10]
    print("\n--- Top Repositories by Stars ---")
    for r in top:
        print(f"  {r['name']}: {r['stargazers_count']} ★ | {r['forks_count']} forks | {r.get('language') or 'N/A'}")

    # Language distribution
    langs = Counter(r.get("language") for r in repos if r.get("language"))
    print("\n--- Language Distribution ---")
    for lang, count in langs.most_common(8):
        print(f"  {lang}: {count} repos")

    # Simple activity score
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    total_forks = sum(r.get("forks_count", 0) for r in repos)
    score = total_stars + total_forks * 2 + user.get("followers", 0) * 3
    print(f"\nDerived Activity Score: {score}")
    print("(stars + 2×forks + 3×followers)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python github_deriver.py <github-username>")
        sys.exit(1)
    derive_user(sys.argv[1])


if __name__ == "__main__":
    main()
