---
name: librenms-mcp
description: Query LibreNMS devices, ports, alerts, inventory, logs and graphs through mcp-server-librenms. Use when asked about network monitoring state in LibreNMS.
---

Start with read-only tools (`devices_*`, `alerts_get`, `ports_*`, `eventlog`/`syslog` tools). The companion package sets `READ_ONLY_MODE=true`, so write tools (create/update/delete, acknowledge alerts, group changes) are hidden; ask the user before disabling read-only mode and confirm before any delete or removal.
