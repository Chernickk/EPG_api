from fastapi import APIRouter, Request, HTTPException, Response

from schemas import CalculatorResult
from service import Evaluator, get_expression_from_query_param
from logger import logger

router = APIRouter()


@router.get('/')
@router.get('/index')
async def root():
    return "Hello world"


@router.get('/eval')
async def calc(phrase: str, request: Request):
    try:
        # Starlette replace "+" with space
        expression = get_expression_from_query_param(request.url.query, 'phrase')
    except ValueError as error:
        logger.debug(error)
        return Response(str(error), 400)
    evaluator = Evaluator(expression)

    try:
        return evaluator.eval()
    except ValueError as error:
        return Response(str(error), 400)
    except ZeroDivisionError as error:
        return Response(str(error), 400)


@router.post('/eval', response_model=CalculatorResult, status_code=201)
async def calc(phrase: str, request: Request):
    try:
        # Starlette replace "+" with space
        expression = get_expression_from_query_param(request.url.query, 'phrase')
    except ValueError as error:
        logger.debug(error)
        raise HTTPException(400, str(error))
    evaluator = Evaluator(expression)

    try:
        return CalculatorResult(
            result=evaluator.eval()
        )
    except ValueError as error:
        raise HTTPException(400, str(error))
    except ZeroDivisionError as error:
        raise HTTPException(400, str(error))
