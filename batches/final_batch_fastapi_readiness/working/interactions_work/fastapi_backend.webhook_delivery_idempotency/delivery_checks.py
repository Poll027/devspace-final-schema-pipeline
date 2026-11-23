import os,tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
import application
# Keep one durable file per scenario, including across new app instances.
def scenario(name):
    with tempfile.TemporaryDirectory() as directory:
        application.DATABASE='sqlite+aiosqlite:///'+str(Path(directory)/'delivery.sqlite')
        app=application.make_app()
        event=application.fixtures['authenticated_events'][0]
        with TestClient(app,raise_server_exceptions=False) as client:
            before=client.portal.call(application.snapshot,app)
            if name=='failure':
                app.state.inject_failure=True
                responses=[client.post('/authenticated-events',json=event)]
            elif name=='concurrent':
                with ThreadPoolExecutor(max_workers=2) as workers:
                    responses=list(workers.map(lambda _:client.post('/authenticated-events',json=event),range(2)))
            else:
                responses=[client.post('/authenticated-events',json=event),client.post('/authenticated-events',json=event)]
            after=client.portal.call(application.snapshot,app)
            # TODO: assert successful acknowledgements, one event identity and
            # one intended state update; failure response must retain before.
        if name=='restart':
            restarted=application.make_app()
            with TestClient(restarted) as client:
                retained=client.portal.call(application.snapshot,restarted)
                response=client.post('/authenticated-events',json=event)
                final=client.portal.call(application.snapshot,restarted)
                # TODO: retained and final equal after, duplicate acknowledged.
if __name__=='__main__':
    import sys
    scenario(sys.argv[1])
