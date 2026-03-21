#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys

from agentpay import NornrWallet, create_mcp_server


def _wallet() -> NornrWallet:
    return NornrWallet.connect(
        api_key=os.environ["NORNR_API_KEY"],
        base_url=os.getenv("NORNR_BASE_URL", "https://nornr.com"),
    )


def _server_name() -> str:
    return f"nornr-{os.getenv('NORNR_AGENT_ID', 'mcp-agent')}"


def _print_json(payload: object) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    argv = list(argv or sys.argv[1:])
    command = argv[0] if argv else "serve"
    env = {
        "NORNR_API_KEY": os.getenv("NORNR_API_KEY", "replace-with-your-key"),
        "NORNR_BASE_URL": os.getenv("NORNR_BASE_URL", "https://nornr.com"),
        "NORNR_AGENT_ID": os.getenv("NORNR_AGENT_ID", "mcp-agent"),
    }

    if command == "serve":
        server = create_mcp_server(_wallet(), server_name=_server_name())
        server.run_stdio()
        return 0
    if command == "manifest":
        server = create_mcp_server(None, server_name=_server_name())
        _print_json(server.build_manifest())
        return 0
    if command == "claude-config":
        server = create_mcp_server(None, server_name=_server_name())
        _print_json(
            server.build_claude_desktop_config(
                command="python3",
                args=[os.path.abspath(__file__), "serve"],
                env=env,
            )
        )
        return 0
    if command == "cursor-config":
        server = create_mcp_server(None, server_name=_server_name())
        _print_json(
            server.build_claude_desktop_config(
                command="python3",
                args=[os.path.abspath(__file__), "serve"],
                env={**env, "NORNR_AGENT_ID": os.getenv("NORNR_AGENT_ID", "cursor-agent")},
            )
        )
        return 0
    print("Usage: python nornr_mcp_control.py [serve|manifest|claude-config|cursor-config]", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
