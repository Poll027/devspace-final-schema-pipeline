"""Offline execution adapter. Statuses are generated, never fixture answers."""
import json
import subprocess
import sys
import yaml
from pathlib import Path

def run_build(config_path, trigger_kind, event):
    config = yaml.safe_load(Path(config_path).read_text())
    triggers = json.loads(Path("triggers.json").read_text())
    trigger = triggers[trigger_kind]
    if trigger_kind == "repository_commit":
        import re
        if re.fullmatch(trigger["branch_filter"], event.get("branch", "")) is None:
            return {"triggered": False, "steps": []}
    elif any(event.get(k) != v for k, v in trigger["filters"].items()):
        return {"triggered": False, "steps": []}
    bindings = dict(config.get("substitutions", {}))
    bindings.update({k: event[field] for k, field in trigger["bindings"].items()})
    results, by_id = [], {}
    pending = list(config["steps"])
    while pending:
        progress = False
        for step in list(pending):
            i = config["steps"].index(step)
            dependencies = step.get("waitFor") or [s["id"] for s in config["steps"][:i]]
            dependencies = [d for d in dependencies if d != "-"]
            if any(d not in by_id for d in dependencies):
                continue
            args = [str(a) for a in step.get("args", [])]
            for j, arg in enumerate(args):
                for key, value in bindings.items():
                    arg = arg.replace("${" + key + "}", str(value)).replace(key, str(value))
                args[j] = arg
            record = {"id": step["id"], "name": step["name"], "resolved_args": args, "waitFor": dependencies}
            if any(by_id[d]["status"] != "SUCCESS" for d in dependencies):
                record.update(status="NOT_STARTED", exit_code=None, output="")
            else:
                if step.get("allowFailure") or any(x != 0 for x in step.get("allowExitCodes", [])):
                    raise ValueError("required gate failures must be fatal")
                if not args or args[0] != "python":
                    raise ValueError("bounded adapter only supports declared Python entry points")
                p = subprocess.run([sys.executable] + args[1:], text=True, capture_output=True)
                record.update(status="SUCCESS" if p.returncode == 0 else "FAILURE", exit_code=p.returncode, output=p.stdout+p.stderr)
            results.append(record); by_id[step["id"]] = record
            pending.remove(step); progress = True
        if not progress:
            raise ValueError("missing dependency or cycle")
    return {"triggered": True, "resolved_inputs": bindings, "steps": results}
