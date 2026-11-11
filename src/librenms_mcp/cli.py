"""Console entry point: adds --version/--help in front of the upstream server."""

import argparse
import importlib.metadata


def main() -> None:
    try:
        version = importlib.metadata.version("mcp-server-librenms")
    except importlib.metadata.PackageNotFoundError:
        version = "unknown"
    parser = argparse.ArgumentParser(
        prog="mcp-server-librenms",
        description="stdio MCP server for LibreNMS (fork of mhajder/librenms-mcp). "
        "Env: LIBRENMS_URL, LIBRENMS_TOKEN (secret), LIBRENMS_VERIFY_SSL, LIBRENMS_TIMEOUT, "
        "READ_ONLY_MODE, DISABLED_TAGS, MCP_TRANSPORT (default stdio). See server.json.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {version}")
    parser.parse_args()
    from librenms_mcp.server import main as run

    run()
