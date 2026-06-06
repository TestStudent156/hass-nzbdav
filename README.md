# NZBDav for Home Assistant

Read-only monitoring of an [nzbdav](https://github.com/nzbdav-dev/nzbdav)
server via its SABnzbd-compatible API.

## Installation (HACS)

1. HACS → ⋮ → **Custom repositories**.
2. Add `https://github.com/<OWNER>/hass-nzbdav` with category **Integration**.
3. Install **NZBDav**, then restart Home Assistant.
4. Settings → Devices & Services → **Add Integration** → **NZBDav**.

## Configuration

| Field | Notes |
|------|------|
| Host | nzbdav host/IP |
| Port | default `3000` |
| Use SSL | enable for https |
| API key | from the nzbdav **Settings** page (same key Sonarr/Radarr use) |
| Verify SSL | disable for self-signed certs |

Update interval is configurable via the integration's **Configure** dialog.

## Entities

Status, download speed, queue items, remaining/total size, time left,
history count, failed count, version, disk free, and a connectivity
binary sensor.
