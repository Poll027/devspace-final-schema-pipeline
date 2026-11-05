"""Run assemble_tiles then validate_tile for the c1 batch context."""
import json
import subprocess
from pathlib import Path

B = Path("batches/final_batch_008_da_python_core")

# Backup original
orig = (B / "batch_run_context.json").read_text()
c1 = (B / "batch_run_context_c1.json").read_text()

# Swap to c1
(B / "batch_run_context.json").write_text(c1)

try:
    # Step 1: assemble
    r1 = subprocess.run(
        ["python3", "00_FINAL_PIPELINE_CORE/scripts/assemble_tiles.py", str(B)],
        capture_output=True, text=True, timeout=300
    )
    print("=== ASSEMBLE ===")
    print("STDOUT:", r1.stdout)
    print("STDERR:", r1.stderr[:500] if r1.stderr else "")
    print("Return code:", r1.returncode)

    if r1.returncode != 0:
        print("Assemble failed, skipping validate")
    else:
        # Step 2: validate
        r2 = subprocess.run(
            ["python3", "00_FINAL_PIPELINE_CORE/scripts/validate_tile.py", str(B)],
            capture_output=True, text=True, timeout=600
        )
        print("\n=== VALIDATE ===")
        print("STDOUT:", r2.stdout)
        print("STDERR:", r2.stderr[:500] if r2.stderr else "")
        print("Return code:", r2.returncode)
finally:
    # Restore original
    (B / "batch_run_context.json").write_text(orig)
    print("\nRestored batch_run_context.json")
