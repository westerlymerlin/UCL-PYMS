# None

<a id="updater"></a>

# updater

Utilities for interacting with the GitHub Contents API.

This module provides functionality to fetch metadata of a repository file and
download raw file content from the GitHub API. It uses an authenticated request
to ensure proper access and handles caching mechanisms like ETag headers to
improve efficiency.

<a id="updater.Path"></a>

## Path

<a id="updater.Optional"></a>

## Optional

<a id="updater.requests"></a>

## requests

<a id="updater.settings"></a>

## settings

<a id="updater.SECRETS"></a>

## SECRETS

<a id="updater.writesettings"></a>

## writesettings

<a id="updater._github_headers"></a>

#### \_github\_headers

```python
def _github_headers(token: Optional[str] = None)
```

Generate HTTP headers for GitHub API requests.

This function constructs a dictionary of headers required for making
requests to the GitHub API. The headers include a user agent and the
GitHub API version. Optionally, if an authentication token is provided,
it adds an Authorisation header to the request.

<a id="updater.get_file_metadata"></a>

#### get\_file\_metadata

```python
def get_file_metadata()
```

Uses GitHub Contents API to fetch metadata about a repository file.
Returns JSON including: sha, size, name, path, download_url, etc.

<a id="updater.download_file_raw_via_api"></a>

#### download\_file\_raw\_via\_api

```python
def download_file_raw_via_api()
```

Downloads raw file bytes via the GitHub Contents API.
If etag_path is provided and the server returns 304 Not Modified, nothing is downloaded.

