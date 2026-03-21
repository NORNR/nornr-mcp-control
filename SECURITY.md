# Security Notes

## Purpose

This repo is a thin public wrapper around the official NORNR Python SDK.

It exists to make the MCP control server easy to inspect and install.
It does not carry a second hidden implementation of NORNR logic.

## Dependency provenance

- pinned package: `nornr-agentpay==0.1.0`
- import path: `agentpay`
- public source: [NORNR/sdk-py](https://github.com/NORNR/sdk-py)

Review the pinned SDK release before production use if your environment requires supply-chain review.

## Required environment

Required:

- `NORNR_API_KEY`

Optional:

- `NORNR_BASE_URL` defaults to `https://nornr.com`
- `NORNR_AGENT_ID` identifies the local agent or client lane

## Recommended key posture

Create a dedicated NORNR key for this MCP server.

Minimum useful scopes:

- `payments:write`
- `workspace:read`
- `approvals:write`
- `events:read`
- `audit:read`

Add only if your flow needs them:

- `reports:read`
- `webhooks:read`

Do not reuse a broad admin or treasury key if a narrower MCP-specific key is enough.

## Runtime guidance

- start with one consequential tool lane
- prefer `mcp-local-tools-guarded` as the initial pack
- test in a non-production workspace first
- verify that queued results actually stop autonomous flows
- keep raw provider or platform limits enabled as a second defensive layer

## Review rule

If NORNR returns queued, blocked, counterparty risk, proof risk or process risk, do not let the downstream MCP tool action continue automatically.
