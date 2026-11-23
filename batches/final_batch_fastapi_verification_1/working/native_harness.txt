# Native adaptation of the registered termination harness. Run beside exercise.py.
# This report, not the in-process WASM result, establishes termination practice.
import ast
import json
import os
from pathlib import Path
import shlex
import signal
import subprocess
import tempfile
import threading
import time
import httpx

source = Path('exercise.py').read_text().split('import asyncio, inspect, json, ast', 1)[0]
values = {}
for node in ast.parse(source).body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        if node.targets[0].id in ('server_command', 'shutdown_limit'):
            values[node.targets[0].id] = ast.literal_eval(node.value)
command = shlex.split(values['server_command'])
configured = float(command[command.index('--timeout-graceful-shutdown') + 1])
assert configured == values['shutdown_limit']
# Use the registry's controlled request delay to leave time for actual process signaling.
controlled_delay = 2
source += '\nimport json\nrequest_delay = ' + repr(controlled_delay) + '\n'
source += '''
_original_lifespan = app.router.lifespan_context
@asynccontextmanager
async def _observed_lifespan(application):
    try:
        async with _original_lifespan(application):
            yield
    finally:
        print('lifespan_client_closed=' + json.dumps({
            'closed': application.state.client.is_closed,
            'recorded_closed': getattr(application.state, 'client_closed', False)
        }), flush=True)
app.router.lifespan_context = _observed_lifespan
'''
command[command.index('main:app')] = 'main:app'
with tempfile.TemporaryDirectory() as workspace:
    Path(workspace, 'main.py').write_text(source)
    p = subprocess.Popen(command, cwd=workspace, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, start_new_session=True)
    events = []
    ready = threading.Event()
    active = threading.Event()
    finished = threading.Event()
    lock = threading.Lock()
    result = {}
    closure = {}
    def collect():
        for line in p.stdout:
            line = line.strip()
            with lock:
                events.append({'at': time.monotonic(), 'line': line})
                if 'Application startup complete' in line:
                    ready.set()
                if line == 'request_started':
                    active.set()
                if line.startswith('lifespan_client_closed='):
                    closure.update(json.loads(line.split('=', 1)[1]))
    collector = threading.Thread(target=collect, daemon=True)
    collector.start()
    def request():
        try:
            response = httpx.get('http://127.0.0.1:8000/orders/42', timeout=configured + controlled_delay + 10)
            with lock:
                result.update(status=response.status_code, json=response.json())
        except Exception as exc:
            with lock:
                result['error'] = type(exc).__name__
        finally:
            with lock:
                result['finished_at'] = time.monotonic()
                finished.set()
    try:
        if not ready.wait(10):
            raise RuntimeError('startup did not complete')
        t = threading.Thread(target=request, daemon=True)
        t.start()
        if not active.wait(10):
            raise RuntimeError('controlled request did not start')
        with lock:
            # An already-finished request can never count as termination-during-request.
            assert not finished.is_set()
            assert not any(e['line'] == 'request_completed' for e in events)
            assert p.poll() is None
            termination_at = time.monotonic()
            os.killpg(p.pid, signal.SIGTERM)
            signal_sent = True
        t.join(configured + 10)
        p.wait(timeout=configured + 10)
        collector.join(5)
        starts = [e['at'] for e in events if e['line'] == 'request_started']
        completions = [e['at'] for e in events if e['line'] == 'request_completed']
        observed_active = (signal_sent and bool(starts) and starts[0] <= termination_at
            and (not completions or termination_at < completions[0])
            and ('finished_at' not in result or termination_at < result['finished_at']))
        completed_in_limit = (result.get('status') == 200 and 'finished_at' in result
            and 0 <= result['finished_at'] - termination_at < configured)
        client_closed = closure.get('closed') is True and closure.get('recorded_closed') is True
        report = {'configured_limit': configured,
            'termination_at': termination_at,
            'termination_during_active_request': observed_active,
            'response': result, 'response_completed_within_limit': completed_in_limit,
            'lifespan_client_closure': closure, 'closed': client_closed,
            'practice_success': observed_active and completed_in_limit and client_closed,
            'events': events, 'process_returncode': p.returncode}
        print(json.dumps(report, indent=2))
        assert report['practice_success'], 'See response outcome and separate client-closure evidence'
    finally:
        if p.poll() is None:
            os.killpg(p.pid, signal.SIGKILL)
            p.wait()
