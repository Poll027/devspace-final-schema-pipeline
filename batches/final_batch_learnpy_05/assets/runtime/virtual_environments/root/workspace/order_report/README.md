Create a project .venv with the selected Python executable, invoke the environment's interpreter explicitly, inspect its runtime prefixes, and list its installed packages.

Platform: POSIX. Project directory: /workspace/order_report. Selected Python executable: /usr/local/bin/python3. Create .venv here, then explicitly invoke /workspace/order_report/.venv/bin/python for the diagnostic and -m pip list.

The project environment exists, its explicitly invoked interpreter reports sys.prefix != sys.base_prefix as True, and its Python successfully runs -m pip list.
