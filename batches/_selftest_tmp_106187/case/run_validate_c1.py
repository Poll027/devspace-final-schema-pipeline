"""Run validate_tile for the c1 batch context by temporarily swapping batch_run_context.json."""
import json
import subprocess
from pathlib import Path

B = Path("batches/final_batch_008_da_python_core")

# Backup original
orig = (B / "batch_run_context.json").read_text()
c1 = (B / "batch_run_context_c1.json").read_text()

# Swap
(B / "batch_run_context.json").write_text(c1)

try:
    result = subprocess.run(
        ["python3", "00_FINAL_PIPELINE_CORE/scripts/validate_tile.py", str(B)],
        capture_output=True, text=True, timeout=600
    )
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr[:2000] if result.stderr else "")
    print("Return code:", result.returncode)
finally:
    # Restore original
    (B / "batch_run_context.json").write_text(orig)
    print("Restored batch_run_context.json")
