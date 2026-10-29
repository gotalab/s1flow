"""Pure effective endpoint resolution shared by request builders and identity."""
import os

DEFAULT_CLOUDFLARE_RELAY = 'http://localhost:8788'


def cloudflare_relay() -> str:
    """Resolve the app-owned relay at use time, without importing provider code."""
    return os.environ.get('CLEF_RELAY_URL', DEFAULT_CLOUDFLARE_RELAY).rstrip('/')
