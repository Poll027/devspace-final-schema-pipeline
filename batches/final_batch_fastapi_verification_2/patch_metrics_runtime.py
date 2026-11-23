import json
from pathlib import Path
p=Path('batches/final_batch_verification_2/interactions.json')
d=json.loads(p.read_text())
i=next(e['interaction'] for t in d['tiles'] for e in t['interactions'] if e['step_id']=='tile_058.s04')
old='from starlette_prometheus import PrometheusMiddleware, metrics'
scaffold='''# Read-only sandbox adapter: starlette_prometheus is not installed in this runtime.
# This fixture models the documented counter/duration boundary for configuration
# practice; it is not the maintained library or a production replacement.
import sys as _metrics_sys
import time as _metrics_time
from types import ModuleType as _MetricsModule
from starlette.middleware.base import BaseHTTPMiddleware as _MetricsBase
from starlette.responses import Response as _MetricsResponse
from starlette.routing import Match as _MetricsMatch

_metrics_samples = {}

def _metric_add(name, labels, amount):
    key = (name, tuple(sorted(labels.items())))
    _metrics_samples[key] = _metrics_samples.get(key, 0) + amount

class _SandboxPrometheusMiddleware(_MetricsBase):
    def __init__(self, app, filter_unhandled_paths=False):
        super().__init__(app)
        self.filter_unhandled_paths = filter_unhandled_paths

    async def dispatch(self, request, call_next):
        path = None
        for route in request.app.routes:
            match, _ = route.matches(request.scope)
            if match == _MetricsMatch.FULL:
                path = route.path
                break
        if path is None and self.filter_unhandled_paths:
            return await call_next(request)
        labels = {"method": request.method, "path": path or request.url.path}
        _metric_add("requests_total", labels, 1)
        started = _metrics_time.perf_counter()
        status = 500
        try:
            response = await call_next(request)
            status = response.status_code
            _metric_add("request_duration_count", labels, 1)
            _metric_add("request_duration_sum", labels,
                        _metrics_time.perf_counter() - started)
            return response
        finally:
            _metric_add("responses_total", dict(labels, status_code=str(status)), 1)

async def _sandbox_metrics(request):
    lines = ["# TYPE requests counter", "# TYPE responses counter",
             "# TYPE request_duration histogram"]
    for (name, labels), value in sorted(_metrics_samples.items()):
        label_text = ",".join(key + "=" + _metrics_json.dumps(val)
                              for key, val in labels)
        lines.append(name + "{" + label_text + "} " + str(value))
    return _MetricsResponse("\\n".join(lines) + "\\n", media_type="text/plain")

_metrics_adapter = _MetricsModule("starlette_prometheus")
_metrics_adapter.PrometheusMiddleware = _SandboxPrometheusMiddleware
_metrics_adapter.metrics = _sandbox_metrics
_metrics_sys.modules["starlette_prometheus"] = _metrics_adapter

from starlette_prometheus import PrometheusMiddleware, metrics'''
for files in [i['public']['workspace']['files'],i['grading']['solution_files']]:
 for f in files:
  assert f['content'].count(old)==1
  f['content']=f['content'].replace(old,scaffold).replace('Configure the imported third-party instrumentation below.', 'Configure the supplied sandbox instrumentation adapter below.').replace("Select the package's actual samples",'Select the adapter\'s observed samples')
i['public']['prompt']=i['public']['prompt'].replace('Use PrometheusMiddleware and metrics from starlette_prometheus.', 'The sandbox supplies a read-only adapter for the unavailable starlette_prometheus package, modeling its documented measurement boundary; this is configuration practice, not verification of the actual third-party package. Use the supplied PrometheusMiddleware and metrics imports.')
p.write_text(json.dumps(d,indent=2)+'\n')
print('Patched only tile_058.s04 runtime scaffolding and adapter disclosure.')
print('Interactions:',sum(len(t['interactions']) for t in d['tiles']))
from collections import Counter
print(dict(Counter(e['interaction']['type'] for t in d['tiles'] for e in t['interactions'])))
