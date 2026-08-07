#!/usr/bin/env python3
"""Lightweight health-check HTTP server for the Hermes bot container.

Runs alongside the Hermes gateway on a separate port so external monitors
(Azure Container Apps health probes, uptime checks, etc.) can verify the
container is alive and the Obsidian vault is mounted without having to
hit the gateway itself.

Endpoints:
    GET /health        -> 200 JSON {status, vault_size, uptime, vault_mounted}
    GET /vault-status  -> 200 JSON with vault existence + markdown file count
    GET /              -> 200 small JSON pointing at the endpoints

Stdlib only — no third-party deps so the image stays slim.
"""

import json
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


START_TIME = time.time()
VAULT_PATH = os.environ.get("OBSIDIAN_VAULT_PATH", "/vault")
HEALTH_HOST = os.environ.get("HEALTH_HOST", "0.0.0.0")
HEALTH_PORT = int(os.environ.get("HEALTH_PORT", "8080"))


def _count_markdown_files(path: str) -> int:
    """Return the number of *.md files under ``path`` (recursive, no follow)."""
    if not os.path.isdir(path):
        return 0
    count = 0
    try:
        for root, _dirs, files in os.walk(path):
            # Skip the .git directory if the vault is a git checkout
            if os.path.basename(root) == ".git":
                continue
            for name in files:
                if name.endswith(".md"):
                    count += 1
    except OSError:
        return 0
    return count


def _vault_status() -> dict:
    mounted = os.path.isdir(VAULT_PATH)
    md_count = _count_markdown_files(VAULT_PATH) if mounted else 0
    return {
        "vault_path": VAULT_PATH,
        "exists": mounted,
        "markdown_files": md_count,
        "ready": mounted and md_count > 0,
    }


def _build_health_response() -> dict:
    vault = _vault_status()
    return {
        "status": "ok",
        "vault_size": vault["markdown_files"],
        "uptime": round(time.time() - START_TIME, 2),
        "vault_mounted": vault["exists"],
        "vault_ready": vault["ready"],
    }


class HealthHandler(BaseHTTPRequestHandler):
    server_version = "HermesHealth/1.0"

    # ---- helpers ---------------------------------------------------------
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    # ---- HTTP verbs ------------------------------------------------------
    def do_GET(self) -> None:  # noqa: N802 (stdlib naming)
        path = self.path.split("?", 1)[0]

        if path == "/health":
            self._send_json(200, _build_health_response())
        elif path == "/vault-status":
            status_code = 200 if _vault_status()["ready"] else 503
            self._send_json(status_code, _vault_status())
        elif path in ("/", "/index.html"):
            self._send_json(
                200,
                {
                    "service": "hermes-health",
                    "endpoints": ["/health", "/vault-status"],
                },
            )
        else:
            self._send_json(404, {"error": "not_found", "path": path})

    # Quieter logs — the gateway container is already chatty
    def log_message(self, format: str, *args) -> None:  # noqa: A002
        return


def main() -> None:
    server = ThreadingHTTPServer((HEALTH_HOST, HEALTH_PORT), HealthHandler)
    print(
        f"[health_server] listening on {HEALTH_HOST}:{HEALTH_PORT} "
        f"(vault={VAULT_PATH})",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
