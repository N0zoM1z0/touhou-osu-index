"""Small retrying HTTP client built on urllib."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any

USER_AGENT = "touhou-osu-index/0.1 (+https://github.com/N0zoM1z0/touhou-osu-index)"


class HttpError(RuntimeError):
    pass


def request(
    url: str,
    *,
    method: str = "GET",
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    attempts: int = 3,
) -> bytes:
    all_headers = {"Accept": "application/json, text/html;q=0.9", "User-Agent": USER_AGENT}
    all_headers.update(headers or {})
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, data=data, method=method, headers=all_headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            retryable = exc.code == 429 or 500 <= exc.code < 600
            if not retryable or attempt + 1 == attempts:
                raise HttpError(f"HTTP {exc.code} from {url}") from exc
            retry_after = exc.headers.get("Retry-After", "")
            delay = int(retry_after) if retry_after.isdigit() else 3 * (2**attempt)
            time.sleep(min(delay, 30))
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt + 1 == attempts:
                raise HttpError(f"request failed after {attempts} attempts: {url}: {exc}") from exc
            time.sleep(2**attempt)
    raise AssertionError("unreachable")


def get_text(url: str) -> str:
    return request(url).decode("utf-8", errors="replace")


def get_json(url: str, *, headers: dict[str, str] | None = None) -> Any:
    try:
        return json.loads(request(url, headers=headers))
    except json.JSONDecodeError as exc:
        raise HttpError(f"invalid JSON from {url}") from exc
