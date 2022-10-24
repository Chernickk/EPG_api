import re
from fastapi import APIRouter, Request, HTTPException

from schemas import CalculatorResult
from service import Calculator

router = APIRouter()


@router.get('/')
@router.get('/index')
async def root():
    return "Hello world"


@router.get('/eval')
async def calc(phrase: str, request: Request):
    # Starlette replace "+" with space
    expression = re.search('phrase=([0-9()+*/-]*)&?', request.url.query).group(1)
    if not expression:
        raise HTTPException(500, 'Something went wrong, please try another phrase')
    calculator = Calculator(expression)

    return calculator.get_result()


@router.post('/eval', response_model=CalculatorResult, status_code=201)
async def calc(phrase: str, request: Request):
    # Starlette replace "+" with space
    expression = re.search('phrase=([0-9()+*/-]*)&?', request.url.query).group(1)
    if not expression:
        raise HTTPException(400, 'Something went wrong, please try another phrase')
    calculator = Calculator(expression)

    return CalculatorResult(
        result=calculator.get_result()
    )
