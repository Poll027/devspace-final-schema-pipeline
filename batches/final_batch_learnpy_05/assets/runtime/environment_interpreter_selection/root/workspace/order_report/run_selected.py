import json
import subprocess
from pathlib import Path
config = json.loads(Path("execution_tool.json").read_text())
raise SystemExit(subprocess.call([config["executable"], "/workspace/order_report/diagnostic.py"]))
