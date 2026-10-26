import json, sys, pathlib, datetime
from importlib.machinery import SourceFileLoader
mod=SourceFileLoader("project_context",str(pathlib.Path(__file__).with_name("project-context.py"))).load_module()
data=json.load(sys.stdin)
try:
    p=mod.project()
    event=data.get("hook_event_name","")
    if event=="PreCompact" and p: mod.checkpoint(p)
    elif event=="PostCompact" and p:
        (p/".context/LAST-COMPACT.md").write_text(str(data.get("compact_summary",""))[:24000],encoding="utf-8")
    elif event=="SessionStart":
        message="Video studio storage: E:/Video. Load scripts/env.ps1 before shell tools. "
        if p: message+=f"Active project: {p}. Read its .context/STATE.md, .context/RENDER.md when present, and only needed manifest sections before continuing. Verify it matches this request. "
        else: message+="No active project selected. Initialize per-project context before editing. "
        message+="Instruction index: plans/CLAUDE-FILE-MAP.md. Before rendering, read the relevant FAST-RENDER-WORKFLOW-v1.md section: colour renders use scripts/render-timeline-colour.py (cut-first GPU route) and delivery uses Export-Instagram balanced (NVENC tuned CQ24, ~89 MB per 80 s).New footage needs fresh colour/masks/content decisions; reuse only matching same-job caches. Preserve the current approved treatment when resuming. "
        print(json.dumps({"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":message}}))
except Exception as e:
    print("Context checkpoint unavailable: "+str(e),file=sys.stderr)
