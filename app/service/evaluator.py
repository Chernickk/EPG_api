import re
from operator import mul, add, sub, truediv

from urllib.parse import unquote

from logger import logger


def get_expression_from_query_param(query_params: str, keyword: str):
    query_params = unquote(query_params)
    query_params = query_params.replace('"', '')
    query_params = query_params.replace("'", '')
    expression = re.search(f'{keyword}=([\S0-9()+*/.-]*)&?', query_params).group(1)
    if not expression:
        raise ValueError("Can't parse phrase, please try another")
    return expression


def get_operator(value: str):
    translator = {
        '/': truediv,
        '*': mul,
        '+': add,
        '-': sub,
    }
    return translator[value]


class Evaluator:
    def __init__(self, phrase: str):
        self.phrase = phrase

    def _eval_part(self, operator: str, expression: str, result_string: str) -> str:
        sub_expr = re.search(f'([\d\.\d]+)\{operator}([\d\.\d]+)', expression)
        try:
            a, b = sub_expr.groups()
        except AttributeError as error:
            raise ValueError('Incorrect number in expression')
        result = get_operator(operator)(float(a), float(b))
        result_string = result_string.replace(sub_expr.group(0), str(result), 1)
        return self.evaluate_expression(result_string)

    def evaluate_expression(self, expression: str) -> str:
        result_string = expression
        splitted = re.findall('[*/]+', expression)
        for operator in splitted:
            return self._eval_part(operator, expression, result_string)

        splitted = re.findall('[+-]+', expression)
        for operator in splitted:
            return self._eval_part(operator, expression, result_string)
        return result_string

    def remove_parentheses(self, phrase: str) -> str:
        open_bracket_index = None
        close_bracket_index = None

        if '(' in phrase or ')' in phrase:
            for i, symbol in enumerate(phrase):
                if symbol == '(':
                    open_bracket_index = i
                elif symbol == ')':
                    if open_bracket_index is None:
                        raise ValueError('Wrong parentheses')
                    close_bracket_index = i

                if open_bracket_index is not None and close_bracket_index is not None:
                    expression = phrase[open_bracket_index + 1:close_bracket_index]
                    result = self.evaluate_expression(expression)
                    phrase = phrase.replace(phrase[open_bracket_index:close_bracket_index + 1], result, 1)
                    return self.remove_parentheses(phrase)
        return phrase

    @logger.catch(reraise=True)
    def eval(self) -> str:
        try:
            phrase_wo_parentheses = self.remove_parentheses(self.phrase)
            result = float(self.evaluate_expression(phrase_wo_parentheses))
        except RecursionError:
            raise ValueError('Too big expression')
        result = int(result) if result.is_integer() else result
        return f'{self.phrase} = {result}'
