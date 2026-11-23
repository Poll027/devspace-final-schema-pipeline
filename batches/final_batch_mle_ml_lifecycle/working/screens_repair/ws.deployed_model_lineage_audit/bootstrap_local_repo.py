"""Run in the exercise runtime only; creates the supplied local repo fixture."""
from pathlib import Path
import subprocess
import os
root = Path("local_repo")
root.mkdir(exist_ok=True)
(root / "model_source.py").write_text('"""Fictional package source retained for lineage inspection."""\ndef transform(feature):\n    return feature / 5.0\n')
env = dict(os.environ, GIT_AUTHOR_DATE="1700000000 +0000", GIT_COMMITTER_DATE="1700000000 +0000", GIT_CONFIG_NOSYSTEM="1")
def run(*args):
    return subprocess.run(["git", *args], cwd=root, env=env, check=True, capture_output=True, text=True).stdout.strip()
run("init", "--initial-branch=main")
run("config", "user.name", "Fixture Author")
run("config", "user.email", "fixture@example.invalid")
run("config", "core.autocrlf", "false")
run("add", "model_source.py")
run("-c", "commit.gpgsign=false", "commit", "-m", "Authored lineage fixture")
assert run("rev-parse", "HEAD") == 'da89ee877040e427fd3de821dffbdc0abd82017b'
