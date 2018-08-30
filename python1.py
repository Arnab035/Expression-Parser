# dictionary of precedence rules
# all operators have L-R associativity

import re

precedence = { '#' : 9, '*' : 8, '/' : 8, '%' : 8, 
        '+' : 7, '-' : 7, '<<' : 6,
        '>>' : 6, '&' : 5, '^' : 4,
         '|' : 3 }

operators = ['*','/','%','+','-','<<','>>','&','^','|', '#']

right = ['#']  # right-associative unary minus

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def stack_top(stack):
    if stack:
        return stack[-1]
    else:
        return None

def is_higher_precedence(op1, op2):
    return precedence[op1] > precedence[op2]

def is_higher_or_equal_precedence(op1, op2):
    return precedence[op1] >= precedence[op2]


def check_for_unary_minus(list_tokens):
    for i in range(1, len(list_tokens)):
        if list_tokens[i] == '-':
            if list_tokens[i-1] == '(' or list_tokens[i-1] in operators:
                # is unary minus
                list_tokens[i] = '#'
    return list_tokens


def convert_infix_to_postfix(infix_expr):
    tokens = check_for_unary_minus(re.findall(r"[+/*%&\^\|()-]|\w+|[<>]{2}", infix_expr))
    print tokens
    postfix = []
    stack = []
    for token in tokens:
        if is_int(token):
            print token
            postfix.append(int(token))
        elif token == '(':
            stack.append(token)
        elif token == ')':
            top = stack_top(stack)
            while top is not None and top != '(':
                postfix.append(top)
                stack.pop()
                top = stack_top(stack)
            stack.pop()
        else:
            # operator
            if not stack or stack_top(stack) == '(':
                stack.append(token)
            else:
                # stack_top is operator
                top = stack_top(stack)
                if token in right:
                    while top is not None and top not in "()" and is_higher_or_equal_precedence(top, token):
                        postfix.append(top)
                        stack.pop()
                        top = stack_top(stack)
                else:
                    while top is not None and top not in "()" and is_higher_precedence(top, token):
                        postfix.append(top)
                        stack.pop()
                        top = stack_top(stack)
                stack.append(token)
    # end of expression
    top = stack_top(stack)
    while top is not None:
        if top not in "()":
            postfix.append(top)
        stack.pop()
        top = stack_top(stack)
    return postfix


def evaluate(postfix_expr):
    value = []
    for val in postfix_expr:
        if val not in operators:
            value.append(val)
        else:
            if val == '#':
                operand1 = value.pop()
                operand2 = -1
                value.append(eval("{0}{1}{2}".format(operand1, '*', operand2)))
            else:
                operand2 = value.pop()
                operand1 = value.pop()
                value.append(eval("{0}{1}{2}".format(operand1, val, operand2)))
    return value[0]


def get_input():
    open_parentheses = 0
    expr = ""
    while True:
        tokens = raw_input('Enter: ')
        print tokens
        if tokens == '(':
            open_parentheses += 1
            expr += tokens
        elif tokens == ')':
            open_parentheses -= 1
            if open_parentheses == 0:
                expr += tokens
                break
            expr += tokens
        else:
            if tokens not in ['<<','>>'] and len(tokens) > 1:
                print "Enter one character at a time"
                return None
            expr += tokens
    return expr


if __name__ == "__main__":
    expr = get_input()
    if expr is None:
        exit()
    post_expr = convert_infix_to_postfix(expr)
    print post_expr
    result = evaluate(post_expr)
    # pretty output here
    string = expr + " = " + str(result)
    print string

