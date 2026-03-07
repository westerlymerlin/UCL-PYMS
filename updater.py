"""
Utilities for interacting with the GitHub Contents API.

This module provides functionality to fetch metadata of a repository file and
download raw file content from the GitHub API. It uses an authenticated request
to ensure proper access and handles caching mechanisms like ETag headers to
improve efficiency.
"""

from pathlib import Path
from typing import Optional, Tuple
import re
import requests
from requests.auth import HTTPBasicAuth
from app_control import settings, SECRETS, writesettings


def _github_headers(token: Optional[str] = None):
    """
    Generate HTTP headers for GitHub API requests.

    This function creates a dictionary of headers required for making requests to the
    GitHub API. It sets the `User-Agent` header to identify the client and includes the
    `Authorization` header if a token is provided, which is used for authenticated requests.

    """
    headers = {"User-Agent": "pyms-updater/1.0", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _parse_owner_repo_from_contents_url(contents_api_url: str) -> Tuple[str, str]:
    """
    Extracts the owner and repository name from a given GitHub contents API URL.
    """
    m = re.search(r"https://api\.github\.com/repos/([^/]+)/([^/]+)/contents/", contents_api_url)
    if not m:
        raise ValueError(f"Unrecognized GitHub contents API url: {contents_api_url}")
    return m.group(1), m.group(2)


def _parse_lfs_pointer(text: str) -> Optional[Tuple[str, int]]:
    """
    Parses a Git LFS pointer from the given text and extracts the object ID (OID) and size.

    This function checks whether the provided text represents a valid Git LFS pointer.
    If the text starts with the appropriate LFS version header and contains valid `oid`
    and `size` information, it extracts and returns them. Otherwise, it may return None
    or raise a ValueError.
    """
    if not text.startswith("version https://git-lfs.github.com/spec/v1"):
        return None

    oid_match = re.search(r"^oid sha256:([0-9a-f]{64})\s*$", text, flags=re.MULTILINE)
    size_match = re.search(r"^size (\d+)\s*$", text, flags=re.MULTILINE)
    if not oid_match or not size_match:
        raise ValueError("Looks like an LFS pointer, but oid/size could not be parsed")

    return oid_match.group(1), int(size_match.group(1))


def get_file_metadata():
    """
    Fetches metadata of a file from a GitHub repository using a specified API endpoint.

    This function sends an HTTP GET request to the configured GitHub API URL. It uses
    a provided personal access token for authentication and specifies the desired
    branch to fetch metadata for. The metadata is retrieved in JSON format and returned
    to the caller.
    """
    headers = _github_headers(SECRETS['pat_token'])
    headers["Accept"] = "application/vnd.github+json"

    r = requests.get(
        settings['updater']['url'],
        headers=headers,
        params={"ref": settings['updater']['branch']},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def _download_stream_to_path(url: str, headers: dict, out_path: Path, timeout: int = 300) -> Optional[str]:
    """
    Downloads a file stream from a given URL and saves it to the specified path. The function will create
    necessary parent directories if they don't exist, and it uses a temporary file during the download
    process to ensure atomicity. If a "304 Not Modified" response is received, the function will return
    None. The function is intended to handle large file downloads in a memory-efficient manner by processing
    the stream in chunks.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_path.with_suffix(out_path.suffix + ".part")

    with requests.get(url, headers=headers, stream=True, timeout=timeout) as r:
        if r.status_code == 304:
            return None  # not modified
        r.raise_for_status()
        etag = r.headers.get("ETag")

        with open(tmp_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    tmp_path.replace(out_path)
    return etag


def _download_lfs_object(owner: str, repo: str, oid_sha256: str, size: int, out_path: Path) -> bool:
    """
    Downloads a Git Large File Storage (LFS) object, ensuring the latest version is retrieved
    based on the provided `oid_sha256`. If the object has already been downloaded, skips the
    operation. The function handles LFS batch endpoint communication, authentication, and file
    stream downloading to the specified output path. Updates internal settings upon successful
    download.
    """
    if settings['updater'].get('sha') == oid_sha256:
        return False

    batch_url = f"https://github.com/{owner}/{repo}.git/info/lfs/objects/batch"

    # LFS endpoints commonly use Basic auth; PAT must have access to the repo.
    # IMPORTANT: keep secrets out of code; we read from SECRETS/settings as you already do.
    auth = HTTPBasicAuth("x-access-token", SECRETS["pat_token"])

    batch_headers = {
        "User-Agent": "pyms-updater/1.0",
        "Accept": "application/vnd.git-lfs+json",
        "Content-Type": "application/vnd.git-lfs+json",
    }

    payload = {
        "operation": "download",
        "transfers": ["basic"],
        "objects": [{"oid": oid_sha256, "size": size}],
    }

    r = requests.post(batch_url, headers=batch_headers, json=payload, auth=auth, timeout=30)
    r.raise_for_status()
    data = r.json()

    obj = (data.get("objects") or [{}])[0]
    if obj.get("error"):
        raise RuntimeError(f"LFS error: {obj['error']}")

    actions = obj.get("actions") or {}
    download = actions.get("download") or {}
    href = download.get("href")
    action_headers = download.get("header") or {}

    if not href:
        raise RuntimeError("LFS batch response missing download href")

    # Download the actual bytes from LFS storage
    _download_stream_to_path(href, headers=action_headers, out_path=out_path, timeout=600)

    settings['updater']['sha'] = oid_sha256
    writesettings()
    return True


def download_file_raw_via_api():
    """
    Fetches the file via Contents API. If the file is Git LFS, resolves the pointer
    and downloads the real object via the LFS Batch API.
    """
    meta = get_file_metadata()
    download_url = meta.get("download_url")
    if not download_url:
        raise RuntimeError("No download_url in GitHub metadata (is this a file path?)")

    out_path = Path(settings['updater']['out_path'])

    # First download/read what the repo serves (this will be the LFS pointer text for LFS files)
    headers = _github_headers(SECRETS['pat_token'])
    with requests.get(download_url, headers=headers, timeout=60) as r:
        r.raise_for_status()
        text = r.text

    lfs = _parse_lfs_pointer(text)
    if lfs:
        oid_sha256, size = lfs
        owner, repo = _parse_owner_repo_from_contents_url(settings['updater']['url'])
        return _download_lfs_object(owner, repo, oid_sha256, size, out_path)

    # Not LFS: fall back to normal streaming download with ETag caching
    if settings['updater'].get('sha'):
        headers["If-None-Match"] = settings['updater']['sha']

    new_etag = _download_stream_to_path(download_url, headers=headers, out_path=out_path, timeout=300)
    if new_etag is None:
        return False

    if settings['updater'].get('sha') and new_etag:
        settings['updater']['sha'] = new_etag
        writesettings()

    return True


if __name__ == "__main__":

    DOWNLOADED = download_file_raw_via_api()

    if DOWNLOADED:
        print(f"Downloaded to: {settings['updater']['out_path']}")
    else:
        print("Already up to date (ETag matched); download skipped.")
