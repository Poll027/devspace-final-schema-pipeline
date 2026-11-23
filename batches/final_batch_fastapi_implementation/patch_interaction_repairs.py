import json
from pathlib import Path
p = Path('batches/final_batch_implementation/interactions.json')
d = json.loads(p.read_text())
entries = {e['step_id']: e['interaction'] for t in d['tiles'] for e in t['interactions']}
ix = entries['tile_028.s05']
result = ix['grading']['tests'][0]['spec']['expected']['result']
harness = '''# Supplied request-dispatch verification harness: leave unchanged.
import asyncio
import threading
import httpx

execution_contexts = {}

def record_context(part):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    execution_contexts[part] = (threading.get_ident(), id(loop) if loop is not None else None)

@app.get("/verify-shipping")
async def verify_shipping():
    execution_contexts.clear()
    event_loop_context = (threading.get_ident(), id(asyncio.get_running_loop()))
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://verification") as client:
        response = await client.get("/shipping")
    handler_context = execution_contexts["handler"]
    utility_context = execution_contexts["utility"]
    assert handler_context == utility_context, "Handler and direct utility must share a worker context"
    assert handler_context[0] != event_loop_context[0], "Handler must execute outside the event-loop thread"
    assert handler_context[1] is None and utility_context[1] is None, "Neither callable may run in the event-loop context"
    response.raise_for_status()
    return response.json()
'''
for f in ix['public']['workspace']['files'] + ix['grading']['solution_files']:
    content = f['content']
    content = content[:content.index('# Supplied inspection harness, unchanged.')]
    # Supply instrumentation inside both callables, identical in starter/solution.
    content = content.replace('def shipping_utility():\n', 'def shipping_utility():\n    record_context("utility")\n')
    content = content.replace('async def shipping():  # TODO: choose execution mode for blocking I/O.\n', 'async def shipping():  # TODO: choose execution mode for blocking I/O.\n    record_context("handler")\n')
    content = content.replace('\ndef shipping():\n', '\ndef shipping():\n    record_context("handler")\n')
    f['content'] = content + harness
ix['public']['prompt'] = ('Choose normal def for the supplied blocking operation. Dispatch the supplied verification request and confirm that the handler and its directly called utility execute in the same FastAPI worker context, outside the event-loop context. '
    'Request GET /verify-shipping; preserve the shipping result and direct shipping_utility() call. Keep the supplied context recording and request-dispatch harness unchanged. Do not await the blocking utility.')
ix['public']['runtime']['packages'] = ['fastapi', 'httpx']
# Preserve the shipping-result key from the existing artifact. The assertions in
# the supplied harness, not an inspector or a fabricated thread label, grade context.
old_tests = ix['grading']['tests']
ix['grading']['tests'] = [{
    'test_id': old_tests[0]['test_id'], 'kind': 'http_equals',
    'spec': {'requests': [{'method': 'GET', 'path': '/verify-shipping'}], 'expected': {'json': result}},
    'visible': True,
    'message_on_fail': 'The dispatched request must preserve the shipping result and pass the supplied same-worker/outside-event-loop assertions.'
}]
# Native launch is not available in the registered runtime. Keep the planned
# code_exercise and its key; explicitly escalate rather than claim string inspection launches.
entries['tile_037.s07']['public']['prompt'] = (
    'Run uvicorn main:app --host 0.0.0.0 --port 8000 without --reload, and verify that the supplied application starts on that host and port. '
    'Planning blocked: the registered python_asgi runtime cannot launch Uvicorn or bind a socket. This anchor and step require a human planning decision and a native launch-capable runtime with supplied startup verification. The existing command-string inspection does not satisfy this success requirement.')
p.write_text(json.dumps(d, indent=2) + '\n')
from collections import Counter
print('tiles:', len(d['tiles']), 'interactions:', len(entries), 'types:', dict(Counter(x['type'] for x in entries.values())))
