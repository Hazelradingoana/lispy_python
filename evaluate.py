import operator
from tokenize_1 import parse

def create_env():
    env = {
        '+': lambda *a: sum(a),
        '*': operator.mul,
        '-': operator.sub,
        'begin': lambda *x: x[-1],
        '/': operator.truediv,
        '//': operator.floordiv,
        '>':operator.gt, '<':operator.lt, '>=':operator.ge, 
        '<=':operator.le, '=':operator.eq,
        'list': lambda *a: list(a),
        'head': lambda a: a[0],
        'tail': lambda a: a[1:],
        'empty?': lambda l: l == [],
        "count": lambda l: len(l),
        'apply': lambda func, args: func(*args),
        # "println": lambda string: print(string) # TODO : support strings
        }
    return env



def eval(exp, env):
    if isinstance(exp, (int, float)):
        return exp
    elif isinstance(exp, bool):
        return exp
    elif isinstance(exp, str):
        return env[exp]
    elif exp[0] == "define":
        symbol = exp[1]
        value = eval(exp[2], env)
        env[symbol] = value
    elif exp[0] == 'quote':
        return exp[1]
    elif exp[0] == 'if':
        cond = eval(exp[1], env)
        if cond:
            return eval(exp[2], env)
        else:
            return eval(exp[3], env)
    elif exp[0] == "set!":
        variable = exp[1]
        value = eval(exp[2], env)
        env[variable] = value
    elif exp[0] == "lambda":
        parameters = exp[1]
        expression = exp[2]
        return lambda *args: eval(expression, dict(zip(parameters, args)), env)
    elif exp[0] == "defun":
        func_and_args = exp[1]
        expression = exp[2]
        func = func_and_args[0]
        args = func_and_args[1:]
        env[func] = lambda *func_args: eval(expression, dict(zip(args, func_args)), env)
    elif exp[0] == "run":
        file = exp[1]
        with open(file) as f:
            text = f.read()
            return eval(parse(text), env)
    else:
        function = eval(exp[0], env)
        arguments = [eval(sub_exp, env) for sub_exp in exp[1:]]
        return function(*arguments)