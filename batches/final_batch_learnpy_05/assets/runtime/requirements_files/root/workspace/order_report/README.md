Recreate a small project's declared dependencies in a fresh virtual environment, inspect their installed versions, and check the project's documented imports using that environment's interpreter.

Use /workspace/order_report/.venv/bin/python for installation, -m pip list, and import_check.py.

The declared dependencies are installed at their pinned versions, the same interpreter's package listing confirms those versions, and all documented required imports run successfully in the recreated interpreter.
