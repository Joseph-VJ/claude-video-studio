"""Speak MCP over stdio to the locally extracted Concat engine; no model calls."""
import argparse, base64, json, os, queue, subprocess, threading, time
from pathlib import Path

ROOT = Path("E:/Video")
LOG = ROOT / "logs/installation-20261024"
LOG.mkdir(parents=True, exist_ok=True)
p = argparse.ArgumentParser()
p.add_argument("--requests")
a = p.parse_args()
env = os.environ.copy()
env["CONCAT_MCP_ROOTS"] = str(ROOT)
env["APPDATA"] = str(ROOT / "cache/appdata")
env["LOCALAPPDATA"] = str(ROOT / "cache/localappdata")
env["XDG_CONFIG_HOME"] = str(ROOT / "cache/config")
env["XDG_DATA_HOME"] = str(ROOT / "cache/data")
err = open(LOG / "concat-mcp-stderr.log", "a", encoding="utf-8")
proc = subprocess.Popen([str(ROOT / "tools/Concat-0.2.8/concat.exe"), "--mcp", "headless"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=err, text=True,
    encoding="utf-8", env=env, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
messages = queue.Queue()
def read_loop():
    for line in proc.stdout:
        try: messages.put(json.loads(line))
        except json.JSONDecodeError: messages.put({"unparsed": line[:500]})
threading.Thread(target=read_loop, daemon=True).start()
sequence = 0

def request(method, params=None, timeout=90):
    global sequence
    sequence += 1
    ident = sequence
    msg = {"jsonrpc": "2.0", "id": ident, "method": method}
    if params is not None: msg["params"] = params
    proc.stdin.write(json.dumps(msg) + "\n"); proc.stdin.flush()
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try: response = messages.get(timeout=max(.1, deadline-time.monotonic()))
        except queue.Empty: break
        if response.get("id") == ident:
            if "error" in response: raise RuntimeError(response["error"])
            return response.get("result")
    raise TimeoutError(f"MCP request timed out: {method}; exit={proc.poll()}")

try:
    hello = request("initialize", {"protocolVersion": "2025-11-25", "capabilities": {},
        "clientInfo": {"name": "VJ-local-studio-check", "version": "1.0"}})
    proc.stdin.write(json.dumps({"jsonrpc":"2.0","method":"notifications/initialized"})+"\n")
    proc.stdin.flush()
    listing = request("tools/list")
    (LOG / "concat-tools.json").write_text(json.dumps(listing, indent=2), encoding="utf-8")
    version = request("tools/call", {"name": "concat_version", "arguments": {}})
    result = {"initialize": hello, "tool_count":len(listing.get("tools", [])), "version":version, "calls":[]}
    if a.requests:
        for item in json.loads(Path(a.requests).read_text(encoding="utf-8-sig")):
            res = request("tools/call", {"name":item["name"], "arguments":item.get("arguments", {})}, timeout=240)
            for block in res.get("content", []):
                if block.get("type") == "image" and block.get("data"):
                    target = LOG / (item["name"]+"-"+str(sequence)+".png")
                    target.write_bytes(base64.b64decode(block.pop("data")))
                    block["saved_path"] = str(target)
            result["calls"].append({"name":item["name"],"result":res})
            (LOG / "concat-mcp-check.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
            if item["name"] == "export_start":
                payload = res.get("structuredContent")
                if payload is None:
                    payload = json.loads(next(b["text"] for b in res["content"] if b.get("type") == "text"))
                job = payload.get("job") or payload.get("jobId") or payload.get("id")
                if not isinstance(job, str):
                    raise RuntimeError("Unexpected export job response: " + json.dumps(payload))
                for attempt in range(10):
                    waited = request("tools/call", {"name":"export_wait", "arguments":{"job":job,"timeoutSeconds":30}}, timeout=45)
                    result["calls"].append({"name":"export_wait","result":waited})
                    (LOG / "concat-mcp-check.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
                    if waited.get("isError"): raise RuntimeError(json.dumps(waited)[:1500])
                    target = Path(item["arguments"]["output"])
                    if target.exists():
                        probe = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(target)],capture_output=True,text=True,timeout=10)
                        if probe.returncode == 0 and float(probe.stdout.strip() or 0) > 0: break
                else: raise TimeoutError("Export did not produce a complete probed file")

            if res.get("isError"):
                raise RuntimeError(json.dumps(res)[:1500])
    (LOG / "concat-mcp-check.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"connected":True,"tools":result["tool_count"],"version":version,"calls":len(result["calls"])}))
finally:
    proc.terminate()
    try: proc.wait(timeout=10)
    except subprocess.TimeoutExpired: proc.kill(); proc.wait()
    err.close()
