DOMAIN = "solark"

CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_PLANT_ID = "plant_id"
CONF_BASE_URL = "base_url"
CONF_API_URL = "api_url"
CONF_SCAN_INTERVAL = "scan_interval"

# Current SolArk Cloud portal / API (confirmed via www.solarkcloud.com frontend).
DEFAULT_BASE_URL = "https://www.solarkcloud.com"
DEFAULT_API_URL = "https://p2.api.solarkcloud.com"
DEFAULT_SCAN_INTERVAL = 30  # seconds

# Older hosts that Sol-Ark retired / redirected away from.
OBSOLETE_BASE_URLS = {
    "https://www.mysolark.com": DEFAULT_BASE_URL,
    "https://mysolark.com": DEFAULT_BASE_URL,
}
OBSOLETE_API_URLS = {
    "https://ecsprod-api-new.solarkcloud.com": DEFAULT_API_URL,
    "https://ecsprod-api.solarkcloud.com": DEFAULT_API_URL,
}

PLATFORMS = ["sensor"]


def normalize_solark_urls(base_url: str, api_url: str) -> tuple[str, str]:
    """Rewrite retired SolArk hosts to the current defaults."""
    base = (base_url or DEFAULT_BASE_URL).rstrip("/")
    api = (api_url or DEFAULT_API_URL).rstrip("/")
    base = OBSOLETE_BASE_URLS.get(base, base)
    api = OBSOLETE_API_URLS.get(api, api)
    return base, api
