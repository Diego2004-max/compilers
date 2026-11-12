"""AFD didáctico para identificadores y números; la tokenización principal usa Regex.

Las transiciones se exponen para estudiar estados, alfabeto y aceptación.
"""
from dataclasses import dataclass

@dataclass
class DFAResult:
    accepted: bool
    state: str
    trace: list

def identifier_dfa(word):
    state='q0'; trace=[]
    for ch in word:
        if state=='q0': nxt='q1' if ch.isascii() and (ch.isalpha() or ch=='_') else 'ERROR'
        elif state=='q1': nxt='q1' if ch.isascii() and (ch.isalnum() or ch=='_') else 'ERROR'
        else: nxt='ERROR'
        trace.append({'caracter':ch,'desde':state,'hasta':nxt}); state=nxt
    return DFAResult(state=='q1',state,trace)

def number_dfa(word):
    state='q0'; trace=[]
    for ch in word:
        if state=='q0': nxt='entero' if ch.isdigit() and ch.isascii() else 'ERROR'
        elif state=='entero': nxt='entero' if ch.isdigit() and ch.isascii() else 'punto' if ch=='.' else 'ERROR'
        elif state=='punto': nxt='decimal' if ch.isdigit() and ch.isascii() else 'ERROR'
        elif state=='decimal': nxt='decimal' if ch.isdigit() and ch.isascii() else 'ERROR'
        else: nxt='ERROR'
        trace.append({'caracter':ch,'desde':state,'hasta':nxt}); state=nxt
    return DFAResult(state in ('entero','decimal'),state,trace)

def analyze_automata(tokens):
    output=[]
    for t in tokens:
        if t.kind in ('ID','NUMBER'):
            dfa=identifier_dfa(t.value) if t.kind=='ID' else number_dfa(t.value)
            output.append({'lexema':t.value,'tipo':t.kind,'aceptado':dfa.accepted,'estado_final':dfa.state,'transiciones':dfa.trace})
    return output

GRAMMAR = '''program     -> statement* EOF
statement   -> TYPE ID '=' expr ';'
             | ID '=' expr ';' | 'print' '(' expr ')' ';'
             | 'free' '(' ID ')' ';' | ID '(' ')' ';'
             | 'fn' ID '(' ')' '{' statement* '}'
             | 'return' expr ';'
expr        -> comparison
comparison  -> addition (('=='|'!='|'<'|'>'|'<='|'>=') addition)*
addition    -> multiply (('+'|'-') multiply)*
multiply    -> unary (('*'|'/') unary)*
unary       -> '-' unary | atom
atom        -> NUMBER | STRING | 'true' | 'false' | ID
             | 'new' '(' NUMBER ')' | '(' expr ')'
TYPE        -> 'int' | 'float' | 'string' | 'bool'
'''
