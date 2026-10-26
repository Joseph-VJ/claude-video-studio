import json,sys
d=json.load(sys.stdin)
cw=d.get("context_window") or {}
used=cw.get("used_percentage")
cost=(d.get("cost") or {}).get("total_cost_usd")
bits=["E: Video"]
if used is not None: bits.append(f"context {used:.0f}%")
if cost is not None: bits.append(f"session ${cost:.2f}")
bits.append("checkpoint before /compact")
print(" | ".join(bits))
