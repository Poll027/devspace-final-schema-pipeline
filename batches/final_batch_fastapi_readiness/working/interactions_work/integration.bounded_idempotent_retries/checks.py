import json
from pathlib import Path
from adapter import Clock,ScriptedTransport,ControlledFailure,execute,server_delay
from starter import policy
fixtures=json.loads(Path('fixtures.json').read_text())
limits=fixtures['hypothetical_limits']
def run(operation,steps):
    clock=Clock(fixtures['receiver_now'])
    transport=ScriptedTransport(steps,clock)
    try:
        result=execute(policy,operation,transport,clock)
    except ControlledFailure:
        result=None
    return result,transport.calls,clock.elapsed
get=fixtures['operations'][0]
post=fixtures['operations'][1]
def transient():
    result,calls,elapsed=run(get,[{'failure':'connect_timeout'},{'result':{'ok':True}}])
    assert result=={'ok':True} and calls==2
    assert 0<elapsed<=limits['max_backoff_seconds']
def delays():
    for value in [fixtures['retry_after_delay_seconds'],fixtures['retry_after_http_date']]:
        expected=server_delay(value,fixtures['receiver_now'])
        result,calls,elapsed=run(get,[{'failure':'http_503','retry_after':value},{'result':{'ok':True}}])
        if expected>=limits['total_time_budget_seconds']:
            assert result is None and calls==1 and elapsed==0
        else:
            assert result=={'ok':True} and calls==2 and elapsed==expected
    result,calls,elapsed=run(get,[{'failure':'http_429','retry_after':str(limits['total_time_budget_seconds']+1)}])
    assert result is None and calls==1 and elapsed==0
def exhaustion():
    result,calls,elapsed=run(get,[{'failure':'read_timeout'}])
    assert result is None and calls==limits['max_attempts']
    assert elapsed<limits['total_time_budget_seconds']
    # Operation duration + next wait must fit too, not merely attempt count.
    result,calls,elapsed=run(get,[{'failure':'read_timeout','duration':limits['total_time_budget_seconds']-1}])
    assert result is None and calls==1
    assert elapsed<limits['total_time_budget_seconds']
def unsafe_post():
    result,calls,elapsed=run(post,[{'failure':'read_timeout'},{'result':{'ok':True}}])
    assert result is None and calls==1 and elapsed==0
    for terminal in ['http_400','http_401','invalid_response']:
        result,calls,elapsed=run(get,[{'failure':terminal},{'result':{'ok':True}}])
        assert result is None and calls==1
if __name__=='__main__':
    import sys
    globals()[sys.argv[1]]()
