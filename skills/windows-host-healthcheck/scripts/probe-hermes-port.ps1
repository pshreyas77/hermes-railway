# probe-hermes-port.ps1
# Find which port Hermes Agent is currently bound to.
# Hermes runs with `--port 0` so it picks dynamically — you can't hardcode it.
#
# Usage (from bash):
#   powershell -NoProfile -ExecutionPolicy Bypass -File probe-hermes-port.ps1
#
# Output: the local port Hermes is listening on, or "NONE" if not running.
# Exit code: 0 if found, 1 if not.

$ports = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
    Where-Object { $_.OwningProcess -in (Get-Process python -ErrorAction SilentlyContinue).Id } |
    Select-Object -ExpandProperty LocalPort -Unique

foreach ($p in $ports) {
    # Hermes typically picks high ephemeral ports. Filter out known non-Hermes ports.
    if ($p -notin 22, 80, 443, 5040, 5354, 5357, 11434) {
        # Sanity check: probe /openapi.json to confirm it's actually Hermes
        $url = "http://127.0.0.1:$p/openapi.json"
        try {
            $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
            if ($resp.Content -match '"title":"Hermes Agent"') {
                Write-Output $p
                exit 0
            }
        } catch {
            # not Hermes on this port, keep looking
        }
    }
}

Write-Output "NONE"
exit 1
