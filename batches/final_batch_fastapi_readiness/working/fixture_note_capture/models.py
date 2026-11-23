from pydantic import BaseModel,Field,ConfigDict
from typing import Literal
class OrderInput(BaseModel):
    id:int=Field(gt=0)
    status:Literal['pending','complete']='pending'
class PublicOrder(BaseModel):
    id:int
    status:Literal['pending','complete']
    model_config=ConfigDict(json_schema_extra={'examples':[{'id':101,'status':'pending'}]})
class ErrorBody(BaseModel):
    detail:str
