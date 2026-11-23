from dataclasses import dataclass
from email.utils import parsedate_to_datetime
from tenacity import Retrying, retry_if_exception
class ControlledFailure(Exception):
    def __init__(self, classification, retry_after=None):
        super().__init__(classification)
        self.classification=classification
        self.retry_after=retry_after
@dataclass
class Clock:
    epoch: float
    elapsed: float=0
    def sleep(self,seconds):
        self.elapsed+=seconds
    def now(self): return self.epoch+self.elapsed
class ScriptedTransport:
    def __init__(self,steps,clock):
        self.steps=list(steps); self.calls=0; self.clock=clock
    def __call__(self):
        self.calls+=1
        step=self.steps[min(self.calls-1,len(self.steps)-1)]
        self.clock.sleep(step.get('duration',0))
        if 'failure' in step:
            raise ControlledFailure(step['failure'],step.get('retry_after'))
        return step.get('result',{'ok':True})
def server_delay(value,now):
    if value is None: return None
    try:
        if str(value).isdigit(): return float(value)
        return max(0,parsedate_to_datetime(value).timestamp()-now)
    except (ValueError,TypeError,OverflowError):
        return None
def execute(policy,operation,transport,clock):
    # Configuration adapter around maintained Tenacity; learners need no loop.
    required=['retryable_failures','max_attempts','total_time_budget','retry_after','bounded_backoff','retry_safe']
    if any(policy.get(key) is None for key in required):
        raise ValueError('Complete all documented policy fields')
    if policy['max_attempts']<1 or policy['total_time_budget']<=0 or policy['bounded_backoff']<0:
        raise ValueError('Finite positive budgets required')
    safe=policy['retry_safe'] and (operation.get('contract_idempotent',False) or operation.get('known_not_applied',False))
    start=clock.elapsed
    def retry(exception):
        return safe and isinstance(exception,ControlledFailure) and exception.classification in policy['retryable_failures']
    def wait(state):
        failure=state.outcome.exception()
        delay=server_delay(failure.retry_after,clock.now()) if policy['retry_after'] else None
        # A valid server delay is not clipped by the client-backoff cap. If it
        # cannot fit in total_time_budget, stop rather than retrying earlier.
        return delay if delay is not None else min(2**(state.attempt_number-1),policy['bounded_backoff'])
    def stop(state):
        return state.attempt_number>=policy['max_attempts'] or clock.elapsed-start+state.upcoming_sleep>=policy['total_time_budget']
    runner=Retrying(retry=retry_if_exception(retry),wait=wait,stop=stop,sleep=clock.sleep,reraise=True)
    return runner(transport)
