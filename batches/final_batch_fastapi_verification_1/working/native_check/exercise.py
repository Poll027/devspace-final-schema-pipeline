request_delay = 0.01
shutdown_limit = 5
import asyncio
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI

async def lifespan(app):
    client = httpx.AsyncClient()
    app.state.client = client
    try:
        yield
    finally:
        await client.aclose()
        app.state.client_closed = client.is_closed
lifespan = asynccontextmanager(lifespan)
app = FastAPI(lifespan=lifespan)

async def controlled_order():
    print('request_started', flush=True)
    await asyncio.sleep(request_delay)
    print('request_completed', flush=True)
    return {'id': 42, 'quantity': 2}
controlled_order = app.get('/orders/42')(controlled_order)

server_command = 'uvicorn main:app --host 127.0.0.1 --port 8000 --timeout-graceful-shutdown 5'
import asyncio, inspect, json, ast
import httpx
from contextlib import contextmanager

def _drive(coro):
    try:
        pending = coro.send(None)
    except StopIteration as done:
        return done.value
    raise RuntimeError('Harness encountered a suspending operation: ' + repr(pending))

async def _requests(application, requests):
    async with application.router.lifespan_context(application):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application, raise_app_exceptions=False), base_url='http://testserver') as client:
            out=[]
            for method,path,kwargs in requests:
                response=await client.request(method,path,**kwargs)
                try: body=response.json()
                except ValueError: body=response.text
                out.append({'status':response.status_code,'body':body})
            return out
def _case(which):
    import shlex
    command=shlex.split(server_command)
    configured=float(command[command.index('--timeout-graceful-shutdown')+1])
    assert configured==shutdown_limit
    async def run():
        async with app.router.lifespan_context(app):
            loop=asyncio.get_running_loop()
            started=loop.time()
            task=asyncio.create_task(controlled_order())
            await asyncio.sleep(0)
            completion_wait_started=loop.time()
            assert not task.done()
            response=await asyncio.wait_for(task,configured)
            elapsed=loop.time()-completion_wait_started
            assert elapsed<configured
        assert app.state.client_closed and app.state.client.is_closed
        return {'configured_limit':configured,'termination_during_active_request':False,'response':response,'closed':app.state.client.is_closed,'verification_mode':'in-process completion and cleanup only'}
    # Expose async verification as an ASGI endpoint for the awaited runner.
    return run()

async def verify_shutdown(which: str): return await _case(which)
verify_shutdown = app.get('/verify-shutdown/{which}')(verify_shutdown)
