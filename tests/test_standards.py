"""MCP server standards (§1, §7): titles, four explicit hints, read-only consistency."""

import asyncio
import importlib
import re

import pytest

HINTS = ("readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint")


@pytest.fixture(scope="module")
def tools(monkeypatch_module=None):
    import os

    os.environ.setdefault("LIBRENMS_URL", "https://librenms.example.invalid")
    os.environ.setdefault("LIBRENMS_TOKEN", "x" * 32)
    os.environ.pop("READ_ONLY_MODE", None)
    server = importlib.import_module("librenms_mcp.server")
    return asyncio.run(server.mcp.list_tools())


def _ann(tool):
    ann = tool.annotations
    return ann.model_dump() if hasattr(ann, "model_dump") else dict(ann or {})


def _get(ann, camel):
    snake = re.sub(r"([A-Z])", lambda m: "_" + m.group(1).lower(), camel)
    return ann.get(camel, ann.get(snake))


def test_every_tool_has_title_and_four_hints(tools):
    assert len(tools) > 100
    for tool in tools:
        assert tool.title and tool.title != tool.name, tool.name
        ann = _ann(tool)
        for hint in HINTS:
            assert _get(ann, hint) is not None, f"{tool.name}: {hint} missing"
        assert not (_get(ann, "readOnlyHint") and _get(ann, "destructiveHint")), tool.name


def test_name_consistency(tools):
    for tool in tools:
        ann = _ann(tool)
        if re.search(r"(^|_)(delete|remove)(_|$)", tool.name):
            assert _get(ann, "destructiveHint"), tool.name


def test_read_only_tag_matches_hint(tools):
    for tool in tools:
        tagged = "read-only" in (tool.tags or set())
        assert tagged == bool(_get(_ann(tool), "readOnlyHint")), tool.name
