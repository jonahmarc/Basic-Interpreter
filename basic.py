import sys
import re
import os

################################

tokens = []
expr_stack = []
symbols = {}

#################################
# CONSTANTS
#################################

DIGITS = '0123456789'
OPERATOR = '+-*/%'
PAREN = '()'

#######################################
# TOKENS
#######################################

TT_PRINT    = 'print'
TT_INPUT    = 'input'

#################################

def open_file(filename):
    os.chdir(r'C:\Users\admin\Downloads')
    data = open(filename, "r").read()
    data += "\n<EOF>"
    return(data)

def lex(filecontents):
    tok = ""
    state = 0
    string = ""
    expr = ""
    isExpr = 0
    n = ""
    varStarted = 0
    var = ""

    filecontents = list(filecontents)

    for char in filecontents:
        tok += char
        if tok == " ":
            if state == 0:
                tok = ""
            else:
                tok = " "
        elif tok == "\n" or tok == "<EOF>":
            if expr != "" and isExpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
            elif expr != "" and isExpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            elif var != "":
                tokens.append("VAR:" + var)
                var = ""
                varStarted = 0
            tok = ""
            isExpr = 0
        elif tok == "=" and state == 0:
            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varStarted = 0
            tokens.append("EQUALS")
            tok = ""
        elif tok == "$" and state == 0:
            varStarted = 1
            var += tok
            tok = ""
        elif varStarted == 1:
            var += tok
            tok = ""
        elif tok == TT_PRINT:
            tokens.append(TT_PRINT)
            tok = "" #reset everytime we find a token
        elif tok == TT_INPUT:
            tokens.append(TT_INPUT)
            tok = ""
        elif tok in DIGITS:
            expr += tok
            tok = ""
        elif tok in OPERATOR or tok in PAREN:
            isExpr = 1
            expr += tok
            tok = ""
        elif tok == "\"" or tok == " \"":
            if state == 0: #we take every letter we find as a part of a keyword/varName
                state = 1
            elif state == 1: #we take every letter we find as a part of a string
                tokens.append("STRING:" + string + "\"")
                string = ""
                state = 0
                tok = ""
        elif state == 1:
            string += tok
            tok = ""
    
    #print(tokens)
    #return ''
    return tokens

def evalExpression(expr):

    regex = r'[-]?\d+|[+/*-]'

    expr_stack = re.findall(regex, expr)
    # print(expr_stack)
    # print(expr)
    return eval(expr)

def doPRINT(toPRINT):
    if(toPRINT[0:6] == "STRING"):
        toPRINT = toPRINT[8:]
        toPRINT = toPRINT[:-1]
    elif(toPRINT[0:3] == "NUM"):
        toPRINT = toPRINT[4:]
    elif(toPRINT[0:4] == "EXPR"):
        toPRINT = evalExpression(toPRINT[5:])
    elif(toPRINT[0:3] == "VAR"):
        toPRINT = toPRINT[8:]
    print(toPRINT)

def doASSIGNvar(varName, varValue):
    symbols[varName[4:]] = varValue

def getVar(varName):
    if varName in symbols:
        return symbols[varName]
    else:
        return ("Undefined Variable")
        exit

def getInput(string, varName):
    i = input(string)
    symbols[varName] = i

def parse(tokens):
    i = 0
    size = len(tokens)
    while( i < size):
        if tokens[i] + " " + tokens[i+1][0:6] == "print STRING" or tokens[i] + " " + tokens[i+1][0:3] == "print NUM" or tokens[i] + " " + tokens[i+1][0:4] == "print EXPR" or tokens[i] + " " + tokens[i+1][0:3] == "print VAR":
            if tokens[i+1][0:6] == "STRING":
                doPRINT(tokens[i+1])
            elif tokens[i+1][0:3] == "NUM":
                doPRINT(tokens[i+1])
            elif tokens[i+1][0:4] == "EXPR":
                doPRINT(tokens[i+1])
            elif tokens[i+1][0:3] == "VAR":
                doPRINT(getVar(tokens[i+1][4:]))
            i += 2
        # execute input function without string instructions
        elif tokens[i] + " " + tokens[i+1][0:3] == "input VAR":
            getInput("", tokens[i+1][4:])
            i+=2
        elif tokens[i][0:3] + " " + tokens[i+1] + " " + tokens[i+2][0:6] == "VAR EQUALS STRING" or tokens[i][0:3] + " " + tokens[i+1] + " " + tokens[i+2][0:3] == "VAR EQUALS NUM" or tokens[i][0:3] + " " + tokens[i+1] + " " + tokens[i+2][0:4] == "VAR EQUALS EXPR":
            if tokens[i+2][0:6] == "STRING":
                doASSIGNvar(tokens[i], tokens[i+2])
            elif tokens[i+2][0:3] == "NUM":
                doASSIGNvar(tokens[i], tokens[i+2])
            elif tokens[i+2][0:4] == "EXPR":
                doASSIGNvar(tokens[i], "NUM:" + str(evalExpression(tokens[i+2][5:])))
            i += 3
         # execute input function with string instructions
        elif tokens[i] + " " + tokens[i+1][0:6] + " " + tokens[i+2][0:3] == "input STRING VAR":
            getInput(tokens[i+1][7:], tokens[i+2][4:])
            i+=3
    # print(symbols)


def run():
    data = open_file('test.lang')
    tokens = lex(data)
    parse(tokens)

run()