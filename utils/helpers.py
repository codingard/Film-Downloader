from urllib.parse import urlparse

def extract_slug_from_url(url: str) -> str:
    path = urlparse(url).path
    parts = path.strip("/").split("/")
    last = parts[-1]
    slug = last.split("-", 1)[-1].replace(".html", "")
    return f"{slug}.mp4"
