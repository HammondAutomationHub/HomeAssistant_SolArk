"""Discover the live SolArk Cloud API base URL from the portal frontend."""
from __future__ import annotations

import logging
import re
from typing import Optional

import aiohttp

_LOGGER = logging.getLogger(__name__)

_APP_JS_RE = re.compile(
    r"""['"](/static/js/app\.[^'"]+\.js)['"]""",
    re.IGNORECASE,
)
_BASE_API_RE = re.compile(
    r"""VUE_APP_BASE_API\s*:\s*["'](https://[^"']+)["']"""
)
_AXIOS_BASE_RE = re.compile(
    r"""create\(\s*\{\s*baseURL\s*:\s*["'](https://[^"']*solarkcloud[^"']*)["']"""
)


async def discover_api_url(
    session: aiohttp.ClientSession,
    base_url: str,
    *,
    timeout: float = 20,
) -> Optional[str]:
    """Return the portal's configured API root, or None if discovery fails."""
    portal = base_url.rstrip("/")
    try:
        async with session.get(
            f"{portal}/",
            timeout=aiohttp.ClientTimeout(total=timeout),
            headers={"Accept": "text/html"},
        ) as resp:
            html = await resp.text()
            resp.raise_for_status()
    except Exception as err:  # noqa: BLE001
        _LOGGER.warning("SolArk API discovery failed fetching portal %s: %s", portal, err)
        return None

    match = _APP_JS_RE.search(html)
    if not match:
        _LOGGER.warning("SolArk API discovery: no app.*.js found at %s", portal)
        return None

    app_js_url = f"{portal}{match.group(1)}"
    try:
        async with session.get(
            app_js_url,
            timeout=aiohttp.ClientTimeout(total=timeout),
            headers={"Accept": "*/*"},
        ) as resp:
            js = await resp.text()
            resp.raise_for_status()
    except Exception as err:  # noqa: BLE001
        _LOGGER.warning(
            "SolArk API discovery failed fetching %s: %s", app_js_url, err
        )
        return None

    api_match = _BASE_API_RE.search(js) or _AXIOS_BASE_RE.search(js)
    if not api_match:
        _LOGGER.warning(
            "SolArk API discovery: no API base found in %s", app_js_url
        )
        return None

    api_url = api_match.group(1).rstrip("/")
    _LOGGER.info("Discovered SolArk API URL from %s: %s", portal, api_url)
    return api_url
