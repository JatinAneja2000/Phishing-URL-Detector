import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = [
    "login", "verify", "secure", "account", "update", "confirm",
    "bank", "password", "signin", "bonus", "free", "gift", "wallet"
]

SUSPICIOUS_EXTENSIONS = [".exe", ".zip", ".rar", ".scr", ".apk"]


def clean_url(url: str) -> str | None:
    url = str(url).strip().lower()

    if not url:
        return None

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        parsed = urlparse(url)

        if not parsed.netloc:
            return None

        return url

    except ValueError:
        return None


def extract_features(url: str) -> dict | None:
    url = clean_url(url)

    if url is None:
        return None

    try:
        parsed = urlparse(url)
    except ValueError:
        return None

    hostname = parsed.netloc
    path = parsed.path

    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"

    return {
        "url_length": len(url),
        "hostname_length": len(hostname),
        "path_length": len(path),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_digits": sum(character.isdigit() for character in url),
        "num_slashes": url.count("/"),
        "num_query_params": len(parsed.query.split("&")) if parsed.query else 0,
        "has_at_symbol": int("@" in url),
        "has_ip_address": int(bool(re.match(ip_pattern, hostname))),
        "uses_https": int(parsed.scheme == "https"),
        "has_suspicious_word": int(any(word in url for word in SUSPICIOUS_WORDS)),
        "has_suspicious_extension": int(
            any(path.endswith(extension) for extension in SUSPICIOUS_EXTENSIONS)
        ),
        "has_multiple_subdomains": int(hostname.count(".") > 2),
    }