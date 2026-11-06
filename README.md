# GitHub Deriver & Push Tools

Two simple Python programs for working with GitHub:

1. **github_deriver.py** - Derive insights from a GitHub user's public profile and repositories.
2. **push_to_github.py** - Push files to a GitHub repository using the REST API.

## Setup

```bash
pip install requests
export GITHUB_TOKEN=your_personal_access_token
```

Get a token at: https://github.com/settings/tokens (needs `repo` scope for pushing).

## Usage

### Analyze a user
```bash
python github_deriver.py xudaniel
```

### Push files via API
```bash
python push_to_github.py
```

Edit the `OWNER`, `REPO`, and file content inside `push_to_github.py` as needed.

## Notes
- Both scripts use the public GitHub REST API.
- Rate limits apply; using a token raises the limit significantly.
- The push script handles create and update (requires existing file SHA for updates).
