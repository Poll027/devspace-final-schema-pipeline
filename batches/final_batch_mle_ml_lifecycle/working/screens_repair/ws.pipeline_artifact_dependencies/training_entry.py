"""Existing training entry point, kept unchanged by dataset-gate exercises."""
import json
import sys
from pathlib import Path
if __name__ == "__main__":
    snapshot_id = sys.argv[1]
    Path("training_invocation.json").write_text(json.dumps({"snapshot_id": snapshot_id, "started": True}))
