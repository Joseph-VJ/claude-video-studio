"""Small project checkpoints; no transcript or media copies."""
import argparse, json, pathlib, re, shutil, datetime
ROOT=pathlib.Path("E:/Video")
POINTER=ROOT/".context/active-project.txt"
def project(value=None):
    raw=value or (POINTER.read_text().strip() if POINTER.exists() else "")
    if not raw: return None
    p=pathlib.Path(raw).resolve()
    if not p.is_relative_to((ROOT/"projects").resolve()): raise ValueError("Project must be inside E:/Video/projects")
    return p
def checkpoint(p):
    target=p/".context/checkpoints"/datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    target.mkdir(parents=True)
    for name in ["STATE.md","DECISIONS.md","ASSET-REQUESTS.md","RENDER.md","DESIGN.md","manifest.json"]:
        src=p/".context"/name
        if src.is_file(): shutil.copy2(src,target/name)
    return str(target)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("action",choices=["init","activate","status","checkpoint","disk"])
    ap.add_argument("--project")
    ap.add_argument("--no-activate",action="store_true",help="Initialize notes without switching the active project")
    a=ap.parse_args()
    if a.no_activate and a.action!="init":ap.error("--no-activate is only valid with init")
    if a.action=="disk":
        print(json.dumps({d:{"free_gib":round(shutil.disk_usage(d).free/2**30,2)} for d in ["C:/","D:/","E:/"]}));return
    p=project(a.project)
    if not p: print("No active project. Use init --project E:/Video/projects/NAME");return
    if a.action=="init":
        (p/".context").mkdir(parents=True,exist_ok=True)
        for d in ["assets/requests","assets/incoming","assets/processed","cache","out","qa"]: (p/d).mkdir(parents=True,exist_ok=True)
        templates={
        "STATE.md":"# Current state\n\nGoal: not specified\nAudience: not established\nSource files: not inspected\nCurrent stage: briefing\nTimeline owner: not selected\nLatest output: none\nVerified checks: none\nPending assets: none\nNext action: inspect the brief and source footage\n",
        "RENDER.md":"# Render handoff\n\nContract: E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md\nSource/cut identity: not inspected\nCurrent-job colour/masks/temporal state: not selected; never inherit a prior video\nTool routes/profile: not selected; inspect current footage and validate a sample\nCache keys/runtime identity: none\nApproved audio/master: none\nStage timings: not measured\nExact output/hash: none\nQA: not performed\nNext action: inspect the current source and record an explicit render plan\n",
        "DESIGN.md":"# Design constitution\n\nNot written. Use /video-design: derive palette, type, surfaces, icon system and motion grammar from this footage (template: E:/Video/.claude/skills/video-design/templates/design-constitution.md). Never inherit another video's design unless the brief says so.\n",
        "DECISIONS.md":"# Decisions\n\nRecord dated choices, source anchors, reasons and superseded decisions here.\n",
        "ASSET-REQUESTS.md":"# Asset requests\n\nUse unique IDs. Record purpose, timeline placement, prompt path, expected filename, status, rights/provenance and QA.\n",
        "manifest.json":json.dumps({"project":str(p),"schema_version":2,"assets":[],"outputs":[],"render_policy":{"workflow":"E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md","handoff":str(p/".context/RENDER.md"),"status":"not-planned"}},indent=2)}
        for name,content in templates.items():
            dest=p/".context"/name
            if not dest.exists(): dest.write_text(content,encoding="utf-8")
    if a.action in ["init","activate"] and not a.no_activate:
        if not (p/".context/STATE.md").exists(): raise ValueError("Initialize project first")
        POINTER.parent.mkdir(parents=True,exist_ok=True);POINTER.write_text(str(p),encoding="utf-8")
    if a.action=="checkpoint": print(checkpoint(p))
    else:
        state=p/".context/STATE.md"
        print(json.dumps({"project":str(p),"state":state.read_text(encoding="utf-8")[:5000] if state.exists() else "not initialized","render_handoff":str(p/".context/RENDER.md"),"render_workflow":"E:/Video/plans/FAST-RENDER-WORKFLOW-v1.md"}))
if __name__=="__main__": main()
