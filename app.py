import os
import math
import requests
from flask import Flask, request, Response, abort
from flask import send_from_directory


app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")





def get_github_headers():
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def fetch_repos(username):
    """
    Fetch public repos for a user (owner type, non-archived).
    Handles simple pagination.
    """
    repos = []
    page = 1
    headers = get_github_headers()

    while True:
        params = {
            "per_page": 100,
            "page": page,
            "type": "owner",
            "sort": "pushed",
            "direction": "desc",
        }
        url = f"{GITHUB_API_URL}/users/{username}/repos"
        r = requests.get(url, headers=headers, params=params, timeout=10)

        if r.status_code != 200:
            raise ValueError(f"GitHub API error: {r.status_code} {r.text}")

        batch = r.json()
        if not batch:
            break

        # Optional: skip forks / archived repos
        for repo in batch:
            if repo.get("fork"):
                continue
            if repo.get("archived"):
                continue
            repos.append(repo)

        page += 1

        # safety limit: don’t loop forever
        if page > 10:  # up to 1000 repos
            break

    return repos


def fetch_language_stats(username):
    """
    Returns a dict: {language: total_bytes} across all repos.
    """
    headers = get_github_headers()
    repos = fetch_repos(username)
    lang_totals = {}

    for repo in repos:
        owner = repo["owner"]["login"]
        name = repo["name"]
        lang_url = f"{GITHUB_API_URL}/repos/{owner}/{name}/languages"

        r = requests.get(lang_url, headers=headers, timeout=10)
        if r.status_code != 200:
            # Just skip repos that error
            continue

        lang_data = r.json()  # { "Python": 12345, "HTML": 6789, ... }
        for lang, bytes_count in lang_data.items():
            lang_totals[lang] = lang_totals.get(lang, 0) + bytes_count

    return lang_totals


def generate_svg(username, lang_totals, top_n=5):
    """
    Build a simple SVG card showing top N languages with percentages and bars.
    """
    if not lang_totals:
        return f"""<svg width="400" height="80" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{ font: 600 16px sans-serif; }}
    .subtitle {{ font: 400 12px sans-serif; fill: #555; }}
  </style>
  <rect width="100%" height="100%" rx="10" ry="10" fill="#fff" stroke="#e4e2e2"/>
  <text x="20" y="35" class="title">Top Languages</text>
  <text x="20" y="55" class="subtitle">@{username} has no language data.</text>
</svg>"""

    total_bytes = sum(lang_totals.values())
    # Sort languages by bytes desc and keep top N
    sorted_langs = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Layout
    bar_max_width = 260
    bar_height = 16
    line_gap = 10
    top_margin = 40
    left_margin = 20

    num_langs = len(sorted_langs)
    height = top_margin + num_langs * (bar_height + line_gap) + 20

    svg_parts = [
        f'<svg width="400" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        "<style>",
        ".title { font: 600 16px sans-serif; }",
        ".subtitle { font: 400 12px sans-serif; fill: #555; }",
        ".label { font: 400 11px sans-serif; fill: #333; }",
        ".percent { font: 600 11px sans-serif; fill: #000; }",
        "</style>",
        f'<rect width="100%" height="100%" rx="10" ry="10" fill="#fff" stroke="#e4e2e2"/>',
        f'<text x="{left_margin}" y="25" class="title">Top Languages</text>',
        f'<text x="{left_margin}" y="40" class="subtitle">@{username}</text>'
    ]

    y = top_margin
    for lang, bytes_count in sorted_langs:
        percent = (bytes_count / total_bytes) * 100
        bar_width = bar_max_width * (bytes_count / total_bytes)

        # background bar
        svg_parts.append(
            f'<rect x="{left_margin}" y="{y}" width="{bar_max_width}" '
            f'height="{bar_height}" fill="#f0f0f0" rx="5" ry="5" />'
        )
        # value bar
        svg_parts.append(
            f'<rect x="{left_margin}" y="{y}" width="{bar_width:.2f}" '
            f'height="{bar_height}" fill="#4c9aff" rx="5" ry="5" />'
        )

        # language text
        svg_parts.append(
            f'<text x="{left_margin + 5}" y="{y + bar_height - 4}" class="label">{lang}</text>'
        )

        # percent text
        svg_parts.append(
            f'<text x="{left_margin + bar_max_width + 10}" '
            f'y="{y + bar_height - 4}" class="percent">{percent:.1f}%</text>'
        )

        y += bar_height + line_gap

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route("/top-langs")
def top_langs():
    username = request.args.get("username")
    if not username:
        abort(400, "Missing 'username' query parameter")

    try:
        lang_totals = fetch_language_stats(username)
    except ValueError as e:
        abort(500, str(e))

    svg = generate_svg(username, lang_totals, top_n=5)
    return Response(svg, mimetype="image/svg+xml")


if __name__ == "__main__":
    # Run locally: python app.py
    app.run(host="0.0.0.0", port=5000, debug=True)
