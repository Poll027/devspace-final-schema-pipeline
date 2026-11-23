from pydantic import BaseModel, Field
class BatchInput(BaseModel):
    order_ids: list[int]  # TODO: Field(max_length=3), from supplied budget
