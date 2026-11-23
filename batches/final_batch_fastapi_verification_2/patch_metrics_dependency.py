import json
from pathlib import Path
p=Path('batches/final_batch_verification_2/interactions.json')
d=json.loads(p.read_text())
ix=next(i['interaction'] for t in d['tiles'] if t['tile_id']=='tile_058' for i in t['interactions'] if i['step_id']=='tile_058.s04')
old='from starlette_prometheus import PrometheusMiddleware, metrics\nfrom prometheus_client.parser import text_string_to_metric_families'
scaffold='''# Read-only sandbox compatibility scaffold. The pinned runtime does not ship
# starlette_prometheus or prometheus_client. These names implement only the
# documented request/response/duration boundary needed by this exercise;
# this is not the maintained package and does not validate its implementation.
import time
import json
from types import SimpleNamespace
from starlette.responses import Response
from starlette.routing import Match

_metric_samples = {}

def _increment(name, labels, amount):
    key = (name, tuple(sorted(labels.items())))
    _metric_samples[key] = _metric_samples.get(key, 0) + amount

class PrometheusMiddleware:
    def __init__(self, app, filter_unhandled_paths=False):
        self.app = app
        self.filter_unhandled_paths = filter_unhandled_paths

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        matched_path = None
        for route in scope["app"].routes:
            match, child_scope = route.matches(scope)
            if match == Match.FULL:
                matched_path = route.path
                break
        if matched_path is None and self.filter_unhandled_paths:
            return await self.app(scope, receive, send)
        labels = {"method": scope["method"], "path": matched_path or scope["path"]}
        _increment("sandbox_requests_total", labels, 1)
        started = time.perf_counter()
        status = 500
        async def capture(message):
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
            await send(message)
        try:
            await self.app(scope, receive, capture)
        except BaseException:
            _increment("sandbox_responses_total", dict(labels, status_code=str(status)), 1)
            raise
        else:
            _increment("sandbox_responses_total", dict(labels, status_code=str(status)), 1)
            elapsed = time.perf_counter() - started
            _increment("sandbox_duration_count", labels, 1)
            _increment("sandbox_duration_sum", labels, elapsed)
            _increment("sandbox_duration_bucket", dict(labels, le="+Inf"), 1)

async def metrics(request):
    # Prometheus text exposition is generated from actual observed ASGI events.
    types = {"sandbox_requests": "counter", "sandbox_responses": "counter", "sandbox_duration": "histogram"}
    lines = ["# TYPE " + name + " " + kind for name, kind in types.items()]
    for (name, labels), value in sorted(_metric_samples.items()):
        label_text = ",".join(k + "=" + json.dumps(v) for k, v in labels)
        lines.append(name + "{" + label_text + "} " + str(value))
    return Response("\\n".join(lines) + "\\n", media_type="text/plain")

def text_string_to_metric_families(text):
    # Minimal parser for the supplied scaffold's own exposition, not a general
    # replacement for prometheus_client.parser.
    families = {}
    for line in text.splitlines():
        if line.startswith("# TYPE "):
            _, _, name, kind = line.split()
            families[name] = SimpleNamespace(type=kind, samples=[])
        elif line and not line.startswith("#"):
            name, rest = line.split("{", 1)
            label_text, value = rest.split("} ", 1)
            labels = dict((part.split("=", 1)[0], json.loads(part.split("=", 1)[1])) for part in label_text.split(","))
            for family_name, family in families.items():
                if name.startswith(family_name + "_"):
                    family.samples.append(SimpleNamespace(name=name, labels=labels, value=float(value)))
                    break
    return families.values()
'''
for f in ix['public']['workspace']['files'] + ix['grading']['solution_files']:
    assert f['content'].count(old)==1
    f['content']=f['content'].replace(old, scaffold)
# Histogram buckets carry the standard le label; probe only count/sum as before.
# Existing verification selects count/sum for duration evidence, but its bounded
# labels assertion must omit the supplied histogram bucket boundary dimension.
for f in ix['public']['workspace']['files'] + ix['grading']['solution_files']:
    f['content']=f['content'].replace('if sample.labels.get("path") == route:', 'if sample.labels.get("path") == route and "le" not in sample.labels:')
ix['public']['prompt']=ix['public']['prompt'].replace('This exercise uses the maintained starlette_prometheus package and its Prometheus metrics exposition.', 'The pinned sandbox lacks starlette_prometheus and prometheus_client. Read-only compatibility scaffolding supplies the documented middleware and metrics-view names and a limited Prometheus exposition parser; it measures actual ASGI events but is not the maintained package. In a deployed app, import these names from starlette_prometheus as taught. Here, leave the supplied adapter unchanged.')
p.write_text(json.dumps(d,indent=2)+'\n')
print('Patched only tile_058.s04; total interactions:',sum(len(t['interactions']) for t in d['tiles']))
