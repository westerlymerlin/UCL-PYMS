"""
Utilities for interacting with the GitHub Contents API.

This module provides functionality to fetch metadata of a repository file and
download raw file content from the GitHub API. It uses an authenticated request
to ensure proper access and handles caching mechanisms like ETag headers to
improve efficiency.
"""

from pathlib import Path
from typing import Optional
import requests
from app_control import settings, SECRETS, writesettings


def _github_headers(token: Optional[str] = None):
    """
    Generate HTTP headers for GitHub API requests.

    This function constructs a dictionary of headers required for making
    requests to the GitHub API. The headers include a user agent and the
    GitHub API version. Optionally, if an authentication token is provided,
    it adds an Authorisation header to the request.
    """
    headers = {"User-Agent": "pyms-updater/1.0", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_file_metadata():
    """
    Uses GitHub Contents API to fetch metadata about a repository file.
    Returns JSON including: sha, size, name, path, download_url, etc.
    """
    headers = _github_headers(SECRETS['pat_token'])
    headers["Accept"] = "application/vnd.github+json"

    r = requests.get(settings['updater']['url'], headers=headers, params={"ref": settings['updater']['branch']}, timeout=30)
    r.raise_for_status()
    return r.json()


def download_file_raw_via_api():
    """
    Downloads raw file bytes via the GitHub Contents API.
    If etag_path is provided and the server returns 304 Not Modified, nothing is downloaded.
    """
    headers = _github_headers(SECRETS['pat_token'])
    headers["Accept"] = "application/vnd.github.raw+json"

    if settings['updater']['sha']:
        headers["If-None-Match"] = settings['updater']['sha']

    out_path = Path(settings['updater']['out_path'])
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(settings['updater']['url'], headers=headers, params={"ref": settings['updater']['branch']},
                      stream=True, timeout=60) as r:
        if r.status_code == 304:
            return False, headers.get("If-None-Match")

        r.raise_for_status()
        new_etag = r.headers.get("ETag")

        tmp_path = out_path.with_suffix(out_path.suffix + ".part")
        with open(tmp_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

        tmp_path.replace(out_path)

    if settings['updater']['sha'] and new_etag:
        settings['updater']['sha'] = new_etag
        writesettings()

    return True


if __name__ == "__main__":

    meta = get_file_metadata()
    print(f"GitHub file: {meta.get('path')} | sha={meta.get('sha')} | size={meta.get('size')} bytes")

    downloaded = download_file_raw_via_api()

    if downloaded:
        print(f"Downloaded to: {settings['updater']['out_path']}")
    else:
        print("Already up to date (ETag matched); download skipped.")
