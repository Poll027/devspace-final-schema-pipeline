from pydantic import BaseModel, Field
import json
from pathlib import Path
budgets=json.loads(Path('fixtures.json').read_text())['hypothetical_budgets']
class BatchInput(BaseModel):
    order_ids: list[int] = Field(max_length=budgets['batch_size'])
