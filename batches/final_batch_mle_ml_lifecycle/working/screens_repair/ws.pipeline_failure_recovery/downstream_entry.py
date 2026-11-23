"""Supplied downstream execution marker; no gate bypass."""
import json
import sys
from pathlib import Path
if __name__ == "__main__":
    Path("downstream_invocation.json").write_text(json.dumps({"artifact_id": sys.argv[1], "started": True}))
