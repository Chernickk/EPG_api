from pydantic import BaseModel


class CalculatorResult(BaseModel):
    result: str
