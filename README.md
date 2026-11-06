# GitHub Deriver

A simple Python program that derives insights from a GitHub user's public profile and repositories.

## Features
- User overview (name, bio, followers, etc.)
- Top 10 repositories by stars
- Language distribution
- Simple activity score

## Setup
```bash
pip install requests
export GITHUB_TOKEN=your_token_here  # optional, for higher rate limits
python github_deriver.py xudaniel
```

## Example
```bash
python github_deriver.py torvalds
```

This tool only uses public GitHub API endpoints.
