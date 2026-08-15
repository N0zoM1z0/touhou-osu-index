"""Minimal osu! API v2 Client Credentials client."""

from __future__ import annotations

import json
import os
import urllib.parse
from datetime import date
from typing import Iterator

from .classifier import apply_classification
from .http import HttpError, get_json, request
from .models import Entry, normalize_mode

TOKEN_URL = "https://osu.ppy.sh/oauth/token"
API_ROOT = "https://osu.ppy.sh/api/v2"


class MissingCredentials(RuntimeError):
    pass


class OsuApi:
    def __init__(self, client_id: str, client_secret: str) -> None:
        if not client_id or not client_secret:
            raise MissingCredentials("OSU_CLIENT_ID and OSU_CLIENT_SECRET are required")
        self.client_id = client_id
        self.client_secret = client_secret
        self._token: str | None = None

    @classmethod
    def from_env(cls) -> "OsuApi":
        return cls(os.environ.get("OSU_CLIENT_ID", ""), os.environ.get("OSU_CLIENT_SECRET", ""))

    def token(self) -> str:
        if self._token:
            return self._token
        body = urllib.parse.urlencode(
            {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
                "scope": "public",
            }
        ).encode()
        raw = request(
            TOKEN_URL,
            method="POST",
            data=body,
            headers={"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
        )
        payload = json.loads(raw)
        self._token = payload["access_token"]
        return self._token

    def get(self, path: str, params: dict[str, str] | None = None) -> dict:
        query = "?" + urllib.parse.urlencode(params) if params else ""
        return get_json(
            f"{API_ROOT}{path}{query}",
            headers={"Authorization": f"Bearer {self.token()}", "Accept": "application/json"},
        )

    def search(self, query: str, *, max_pages: int = 4) -> Iterator[dict]:
        cursor: str | None = None
        for _ in range(max_pages):
            params = {"q": query}
            if cursor:
                params["cursor_string"] = cursor
            payload = self.get("/beatmapsets/search", params)
            yield from payload.get("beatmapsets", [])
            cursor = payload.get("cursor_string")
            if not cursor:
                break

    def beatmapset(self, beatmapset_id: int) -> dict:
        return self.get(f"/beatmapsets/{beatmapset_id}")


def entry_from_osu(raw: dict, *, evidence: list[str], confidence: str = "candidate") -> Entry:
    modes = sorted({normalize_mode(item.get("mode", "")) for item in raw.get("beatmaps", []) if item.get("mode")})
    entry = Entry(
        beatmapset_id=raw["id"],
        artist=raw.get("artist", ""),
        title=raw.get("title", ""),
        creator=raw.get("creator", ""),
        source=raw.get("source", ""),
        status=raw.get("status", "unknown"),
        modes=modes,
        evidence=evidence,
        confidence=confidence,
        last_checked=date.today().isoformat(),
        osu_last_updated=raw.get("last_updated"),
    )
    return apply_classification(entry, tags=raw.get("tags", ""))
