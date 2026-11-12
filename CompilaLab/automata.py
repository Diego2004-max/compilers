"""AFD didácticos (S2) y gramática del lenguaje (S3-S4).

IMPORTANTE para la sustentación: el lexer de producción (compiler.lex) usa la
regex maestra; estos AFD se ejecutan EN PARALELO sobre los lexemas ya reconocidos
para mostrar, estado por estado, qué máquina hay "debajo" de una regex.

Ruta teórica completa (S2):  RegEx ─Thompson─► AFN ─subconjuntos─► AFD ─Hopcroft─► AFD mínimo
Aquí se escriben directamente los AFD mínimos de dos patrones; la construcción
automática (Thompson, subconjuntos, Hopcroft) no está implementada.
"""
from dataclasses import dataclass


@dataclass
class DFAResult:
    accepted: bool
    state: str
    trace: list


def char_class(ch):
    """Alfabeto de entrada COMPRIMIDO: en vez de una columna por carácter (256+),
    la tabla tiene una columna por clase. Es la misma idea que usan los generadores
    de lexers (flex) para que la matriz quepa en memoria."""
    if ch.isascii() and (ch.isalpha() or ch == '_'):
        return 'letra'
    if ch.isascii() and ch.isdigit():
        return 'digito'
    if ch == '.':
        return 'punto'
    return 'otro'


# Matrices de transición δ(estado, clase) → estado.  [S2 "Simulación de matriz de transición"]
# Una celda que NO existe equivale a ir al estado sumidero ERROR (rechazo).
IDENTIFIER_TABLE = {
    'q0': {'letra': 'q1'},                       # un ID no puede empezar con dígito: "2vida" es error léxico
    'q1': {'letra': 'q1', 'digito': 'q1'},
}
IDENTIFIER_ACCEPT = {'q1'}

NUMBER_TABLE = {
    'q0':      {'digito': 'entero'},
    'entero':  {'digito': 'entero', 'punto': 'punto'},
    'punto':   {'digito': 'decimal'},            # "1." se queda en 'punto', que NO acepta
    'decimal': {'digito': 'decimal'},            # un segundo '.' no tiene celda → ERROR ("1.2.3")
}
NUMBER_ACCEPT = {'entero', 'decimal'}


def run_dfa(table, accepting, word, start='q0'):
    """Simulador genérico: O(n) en la longitud del lexema y O(1) por paso
    (una búsqueda en la tabla). No hay retroceso: eso es lo que gana un AFD frente a un AFN."""
    state, trace = start, []
    for ch in word:
        nxt = table.get(state, {}).get(char_class(ch), 'ERROR')
        trace.append({'caracter': ch, 'desde': state, 'hasta': nxt})
        state = nxt
        if state == 'ERROR':
            # El sumidero no tiene salida: el resto del lexema ya no puede ser aceptado.
            break
    return DFAResult(state in accepting, state, trace)


def identifier_dfa(word):
    return run_dfa(IDENTIFIER_TABLE, IDENTIFIER_ACCEPT, word)


def number_dfa(word):
    return run_dfa(NUMBER_TABLE, NUMBER_ACCEPT, word)


def analyze_automata(tokens):
    """Recorre los tokens ID/NUMBER y documenta la traza de su AFD (pestaña Autómatas)."""
    output = []
    for t in tokens:
        if t.kind in ('ID', 'NUMBER'):
            dfa = identifier_dfa(t.value) if t.kind == 'ID' else number_dfa(t.value)
            output.append({'lexema': t.value, 'tipo': t.kind, 'aceptado': dfa.accepted,
                           'estado_final': dfa.state, 'transiciones': dfa.trace})
    return output


# Gramática en EBNF. Cada no terminal es una función del compiler.Parser.
# Niveles de expresión de MENOR a MAYOR precedencia: más abajo = se agrupa primero.
# (?) ¿Por qué esto es libre de contexto y no regular? Por '(' expr ')': los paréntesis
#     anidados necesitan "contar", y un autómata finito no tiene pila (S4).
GRAMMAR = '''program     -> statement* EOF
statement   -> TYPE ID '=' expr ';'
             | ID '=' expr ';' | 'print' '(' expr ')' ';'
             | 'free' '(' ID ')' ';' | ID '(' ')' ';'
             | 'fn' ID '(' ')' '{' statement* '}'
             | 'return' expr ';'
expr        -> logic_or
logic_or    -> logic_and ('||' logic_and)*
logic_and   -> comparison ('&&' comparison)*
comparison  -> addition (('=='|'!='|'<'|'>'|'<='|'>=') addition)*
addition    -> multiply (('+'|'-') multiply)*
multiply    -> unary (('*'|'/') unary)*
unary       -> '-' unary | '!' unary | atom
atom        -> NUMBER | STRING | 'true' | 'false' | ID
             | 'new' '(' NUMBER ')' | '(' expr ')'
TYPE        -> 'int' | 'float' | 'string' | 'bool'
'''
