"""Constants for the NZBDav integration."""
from __future__ import annotations

DOMAIN = "nzbdav"

# Config entry keys
CONF_HOST = "host"
CONF_PORT = "port"
CONF_SSL = "ssl"
CONF_API_KEY = "api_key"
CONF_VERIFY_SSL = "verify_ssl"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_PORT = 3000
DEFAULT_SSL = False
DEFAULT_VERIFY_SSL = True
DEFAULT_SCAN_INTERVAL = 30  # seconds

MANUFACTURER = "nzbdav-dev"
MODEL = "NZBDav"
