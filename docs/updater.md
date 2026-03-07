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

<a id="updater.Tuple"></a>

## Tuple

<a id="updater.re"></a>

## re

<a id="updater.requests"></a>

## requests

<a id="updater.HTTPBasicAuth"></a>

## HTTPBasicAuth

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

This function creates a dictionary of headers required for making requests to the
GitHub API. It sets the `User-Agent` header to identify the client and includes the
`Authorization` header if a token is provided, which is used for authenticated requests.

<a id="updater._parse_owner_repo_from_contents_url"></a>

#### \_parse\_owner\_repo\_from\_contents\_url

```python
def _parse_owner_repo_from_contents_url(
        contents_api_url: str) -> Tuple[str, str]
```

Extracts the owner and repository name from a given GitHub contents API URL.

<a id="updater._parse_lfs_pointer"></a>

#### \_parse\_lfs\_pointer

```python
def _parse_lfs_pointer(text: str) -> Optional[Tuple[str, int]]
```

Parses a Git LFS pointer from the given text and extracts the object ID (OID) and size.

This function checks whether the provided text represents a valid Git LFS pointer.
If the text starts with the appropriate LFS version header and contains valid `oid`
and `size` information, it extracts and returns them. Otherwise, it may return None
or raise a ValueError.

<a id="updater.get_file_metadata"></a>

#### get\_file\_metadata

```python
def get_file_metadata()
```

Fetches metadata of a file from a GitHub repository using a specified API endpoint.

This function sends an HTTP GET request to the configured GitHub API URL. It uses
a provided personal access token for authentication and specifies the desired
branch to fetch metadata for. The metadata is retrieved in JSON format and returned
to the caller.

<a id="updater._download_stream_to_path"></a>

#### \_download\_stream\_to\_path

```python
def _download_stream_to_path(url: str,
                             headers: dict,
                             out_path: Path,
                             timeout: int = 300) -> Optional[str]
```

Downloads a file stream from a given URL and saves it to the specified path. The function will create
necessary parent directories if they don't exist, and it uses a temporary file during the download
process to ensure atomicity. If a "304 Not Modified" response is received, the function will return
None. The function is intended to handle large file downloads in a memory-efficient manner by processing
the stream in chunks.

<a id="updater._download_lfs_object"></a>

#### \_download\_lfs\_object

```python
def _download_lfs_object(owner: str, repo: str, oid_sha256: str, size: int,
                         out_path: Path) -> bool
```

Downloads a Git Large File Storage (LFS) object, ensuring the latest version is retrieved
based on the provided `oid_sha256`. If the object has already been downloaded, skips the
operation. The function handles LFS batch endpoint communication, authentication, and file
stream downloading to the specified output path. Updates internal settings upon successful
download.

<a id="updater.download_file_raw_via_api"></a>

#### download\_file\_raw\_via\_api

```python
def download_file_raw_via_api()
```

Fetches the file via Contents API. If the file is Git LFS, resolves the pointer
and downloads the real object via the LFS Batch API.

