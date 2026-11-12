"""CompilaLab: compilador educativo para una CPU virtual de pocos registros.

Pipeline (S1, "Las 6 fases en acción"):

    texto ─► lex() ─► Parser ─► Semantic ─► IRBuilder ─► optimize() ─► Backend ─► VirtualCPU
            tokens     AST      tabla de     TAC /        TAC más       ISA         ejecución
                                símbolos     cuádruplas   pequeño       virtual     verificada

Front-end = lex + Parser + Semantic (depende del lenguaje fuente).
Middle-end = IRBuilder + optimize (independiente del lenguaje y de la máquina).
Back-end = Backend + VirtualCPU (depende de la "arquitectura" destino).

Convención de comentarios de estudio:
    [S#]  semana del curso donde se vio el concepto.
    (?)   pregunta probable en la sustentación, con la idea clave para responderla.
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, asdict


# ════════════════════════════════════════════════════════════════════════════
#  ERRORES — [S1] "Clasificación de errores": cada fase lanza su propia categoría
# ════════════════════════════════════════════════════════════════════════════

class CompileError(Exception):
    """Error con fase + coordenadas. La fase le dice al programador QUÉ filtro falló."""

    def __init__(self, phase, line, column, message):
        super().__init__(f'{phase} (línea {line}, columna {column}): {message}')
        self.phase, self.line, self.column, self.message = phase, line, column, message


# ════════════════════════════════════════════════════════════════════════════
#  FASE 1 · ANÁLISIS LÉXICO — [S2] lexema / token / patrón
# ════════════════════════════════════════════════════════════════════════════

@dataclass
class Token:
    kind: str     # token  = categoría que consume el parser (ID, NUMBER, '+', INT...)
    value: str    # lexema = texto exacto leído del fuente
    line: int
    column: int


# Una sola regex maestra con named groups (?P<NOMBRE>...): el motor `re` prueba las
# alternativas DE IZQUIERDA A DERECHA, así que el orden es la tabla de prioridades:
#   · comentarios antes que el operador '/'      → "//" no se parte en dos '/'
#   · NUMBER acepta el decimal completo           → "3.14" no queda como 3 . 14   [S2 "FLOAT antes que INT"]
#   · STRING antes que UNCLOSED                   → solo cae en UNCLOSED si no hay comilla de cierre en la línea
#   · operadores de 2 caracteres antes que los de 1 → "<=" no se lee como '<' '='
#   · INVALID ('.') al final                     → atrapa cualquier carácter fuera del alfabeto
# Las palabras reservadas NO van en la regex: se reconoce un ID y luego se consulta
# KEYWORDS. Así "integer" no se corta en INT + "eger" (el problema que el \b resolvía en clase).
PATTERN = re.compile(
    r'(?P<COMMENT>//[^\n]*)'
    r'|(?P<BLOCK_COMMENT>/\*[\s\S]*?\*/)'
    r'|(?P<UNCLOSED_COMMENT>/\*)'
    r'|(?P<SPACE>[ \t\r]+)'
    r'|(?P<NEWLINE>\n)'
    r'|(?P<NUMBER>\d+(?:\.\d+)?)'
    r'|(?P<STRING>"(?:[^"\\\n]|\\.)*")'
    r'|(?P<UNCLOSED>"[^"\n]*)'
    r'|(?P<ID>[a-zA-Z_]\w*)'
    r'|(?P<OP>==|!=|<=|>=|&&|\|\||[+*/=;(){}<>,!-])'
    r'|(?P<INVALID>.)'
)
KEYWORDS = {'int', 'float', 'string', 'bool', 'true', 'false',
            'print', 'fn', 'return', 'new', 'free'}


def lex(source):
    """Escanea de izquierda a derecha y devuelve la lista de tokens terminada en EOF.

    Recuperación en "modo pánico" (S2, cláusula ERROR): un carácter inválido no
    detiene el escaneo; se anota y se sigue, para reportar TODOS los errores léxicos
    de una vez. Solo al final se lanza un único CompileError con el primero y el conteo.
    """
    tokens, errors = [], []
    line, col = 1, 1
    for m in PATTERN.finditer(source):
        kind, val = m.lastgroup, m.group()
        if kind == 'NEWLINE':
            line, col = line + 1, 1
            continue
        if kind == 'BLOCK_COMMENT':
            # Un comentario multilínea "consume" saltos de línea: si no se cuentan,
            # todas las coordenadas posteriores quedan corridas (reto de la S2).
            breaks = val.count('\n')
            if breaks:
                line += breaks
                col = len(val) - val.rfind('\n')
            else:
                col += len(val)
            continue
        if kind in ('SPACE', 'COMMENT'):          # ruido: se descarta, pero mueve la columna
            col += len(val)
            continue
        if kind == 'UNCLOSED':
            errors.append((line, col, 'Cadena sin cerrar'))
        elif kind == 'UNCLOSED_COMMENT':
            errors.append((line, col, 'Comentario /* sin cerrar'))
        elif kind == 'INVALID':
            errors.append((line, col, f'Carácter inválido {val!r}'))
        else:
            if kind == 'ID' and val in KEYWORDS:
                kind = val.upper()                # 'int' → token INT
            elif kind == 'OP':
                kind = val                        # el propio símbolo es el tipo de token
            tokens.append(Token(kind, val, line, col))
        col += len(val)
    if errors:
        first_line, first_col, message = errors[0]
        if len(errors) > 1:
            rest = ', '.join(f'L{l}:C{c} {msg}' for l, c, msg in errors[1:4])
            message += f' (+{len(errors) - 1} error(es) léxico(s) más: {rest})'
        raise CompileError('Léxico', first_line, first_col, message)
    tokens.append(Token('EOF', '', line, col))   # centinela: el parser nunca se sale de la lista
    return tokens


# ════════════════════════════════════════════════════════════════════════════
#  FASE 2 · ANÁLISIS SINTÁCTICO — [S3-S4] gramática libre de contexto → AST
# ════════════════════════════════════════════════════════════════════════════

@dataclass
class Node:
    """Nodo del AST. Es ABSTRACTO: no guarda ';', '(' ni ')' porque la forma del
    árbol ya codifica la agrupación (S4: árbol de parseo concreto vs AST)."""
    kind: str
    line: int
    value: object = None
    children: tuple = ()
    column: int = 0

    def json(self):
        return {'kind': self.kind, 'line': self.line, 'column': self.column,
                'value': self.value, 'children': [c.json() for c in self.children]}


class Parser:
    """Descenso recursivo (Top-Down, LL(1)): una función por no terminal.

    Gramática completa en automata.GRAMMAR. La precedencia sale de la PROFUNDIDAD
    de las llamadas: la regla más "abajo" (mul) se reduce primero, así que
    a + b * c produce '+'(a, '*'(b, c)) sin tabla de precedencias.

    (?) ¿Por qué no hay recursión infinita? Las reglas se escribieron en EBNF con
        repetición (X → Y (op Y)*) en vez de X → X op Y; un while reemplaza la
        recursión izquierda que colgaría a un parser Top-Down (S4).
    (?) ¿Y la asociatividad? El while va "acumulando" left = op(left, siguiente),
        por eso 10 - 3 - 2 es (10 - 3) - 2: asociatividad izquierda.
    """

    def __init__(self, tokens):
        self.ts = tokens
        self.i = 0

    # ── utilidades: "mirar" sin consumir (lookahead de 1 token) y "consumir" ──
    def at(self, *kinds):
        return self.ts[self.i].kind in kinds

    def take(self, kind=None):
        t = self.ts[self.i]
        if kind and t.kind != kind:
            raise CompileError('Sintáctico', t.line, t.column,
                               f'Se esperaba {kind}, llegó {t.value or "fin de archivo"!r}')
        self.i += 1
        return t

    def node(self, kind, tok, value=None, children=()):
        return Node(kind, tok.line, value, tuple(children), tok.column)

    # program → statement* EOF
    def parse(self):
        items = []
        while not self.at('EOF'):
            items.append(self.statement())
        return Node('program', 1, children=tuple(items), column=1)

    def statement(self):
        # El PRIMER token decide la producción (conjunto FIRST): eso es lo que
        # hace a la gramática predictiva y evita backtracking.
        t = self.ts[self.i]
        if self.at('INT', 'FLOAT', 'STRING', 'BOOL'):
            typ = self.take().value
            name = self.take('ID')
            self.take('=')
            exp = self.expr()
            self.take(';')
            return self.node('declare', name, {'type': typ, 'name': name.value}, (exp,))
        if self.at('PRINT'):
            self.take(); self.take('(')
            exp = self.expr()
            self.take(')'); self.take(';')
            return self.node('print', t, children=(exp,))
        if self.at('FREE'):
            self.take(); self.take('(')
            name = self.take('ID')
            self.take(')'); self.take(';')
            return self.node('free', name, name.value)
        if self.at('FN'):
            self.take()
            name = self.take('ID')
            self.take('('); self.take(')'); self.take('{')
            body = []
            while not self.at('}', 'EOF'):
                body.append(self.statement())
            self.take('}')                      # si llegó EOF, aquí sale "Se esperaba }"
            return self.node('function', name, name.value, body)
        if self.at('RETURN'):
            self.take()
            exp = self.expr()
            self.take(';')
            return self.node('return', t, children=(exp,))
        if self.at('ID'):
            # ID es ambiguo con 1 token (llamada o asignación); el SEGUNDO token
            # desempata. Por eso se consume el ID y se mira lo que sigue.
            name = self.take()
            if self.at('('):
                self.take('('); self.take(')'); self.take(';')
                return self.node('call', name, name.value)
            self.take('=')
            exp = self.expr()
            self.take(';')
            return self.node('assign', name, name.value, (exp,))
        raise CompileError('Sintáctico', t.line, t.column, f'Sentencia inesperada {t.value!r}')

    # ── expresiones: de MENOR a MAYOR precedencia ──
    #   ||  <  &&  <  comparación  <  + -  <  * /  <  unario  <  átomo
    def expr(self):
        return self.logic_or()

    def binary_level(self, operators, next_level):
        """Plantilla común de los niveles  X → Y (op Y)*  (evita repetir 5 veces el while)."""
        left = next_level()
        while self.at(*operators):
            op = self.take()
            left = self.node('binary', op, op.value, (left, next_level()))
        return left

    def logic_or(self):
        return self.binary_level(('||',), self.logic_and)

    def logic_and(self):
        return self.binary_level(('&&',), self.comparison)

    def comparison(self):
        return self.binary_level(('==', '!=', '<', '>', '<=', '>='), self.add)

    def add(self):
        return self.binary_level(('+', '-'), self.mul)

    def mul(self):
        return self.binary_level(('*', '/'), self.unary)

    def unary(self):
        if self.at('-'):
            # "Azúcar sintáctico": -x se reescribe como 0 - x. Así el resto del
            # compilador no necesita un operador unario aritmético.
            t = self.take()
            return self.node('binary', t, '-', (self.node('number', t, '0'), self.unary()))
        if self.at('!'):
            t = self.take()
            return self.node('not', t, children=(self.unary(),))
        return self.atom()

    def atom(self):
        t = self.ts[self.i]
        if self.at('NUMBER'):
            self.take(); return self.node('number', t, t.value)
        if self.at('STRING'):
            self.take(); return self.node('string', t, t.value[1:-1])   # se quitan las comillas
        if self.at('TRUE', 'FALSE'):
            self.take(); return self.node('boolean', t, t.value == 'true')
        if self.at('ID'):
            self.take(); return self.node('variable', t, t.value)
        if self.at('NEW'):
            self.take(); self.take('(')
            size = self.take('NUMBER')
            self.take(')')
            if '.' in size.value or int(size.value) <= 0:
                raise CompileError('Sintáctico', size.line, size.column, 'new requiere un entero positivo')
            return self.node('new', t, int(size.value))
        if self.at('('):
            # Los paréntesis desaparecen del AST: solo sirven para volver a empezar
            # desde la precedencia más baja (expr) dentro de un factor.
            self.take()
            exp = self.expr()
            self.take(')')
            return exp
        raise CompileError('Sintáctico', t.line, t.column, f'Expresión inesperada {t.value!r}')


# ════════════════════════════════════════════════════════════════════════════
#  FASE 3 · ANÁLISIS SEMÁNTICO — [S5] tabla de símbolos y ámbitos, [S6] tipos
# ════════════════════════════════════════════════════════════════════════════

NUMERIC = {'int', 'float'}
RELATIONAL = ('<', '>', '<=', '>=')
EQUALITY = ('==', '!=')
LOGICAL = ('&&', '||')


class Semantic:
    """Recorre el AST validando SIGNIFICADO: existencia, ámbito y tipos.

    self.scopes es la PILA de ámbitos de la S5: [global, local_de_función].
    Entrar a una función = push de un dict vacío; salir = pop (sus variables "mueren").
    self.symbols es solo el registro histórico que se muestra en la GUI.
    """

    def __init__(self):
        self.scopes = [{}]
        self.symbols = []
        self.functions = {}

    def lookup(self, name, node):
        # Búsqueda léxica: del ámbito actual hacia el global (S5, "vidrio espía":
        # desde adentro se ve hacia afuera, nunca al revés).
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise CompileError('Semántico', node.line, node.column, f'Variable {name!r} no declarada')

    def error(self, node, message):
        raise CompileError('Semántico', node.line, node.column, message)

    # ── [S6] inferencia: cada expresión "sube" su tipo desde las hojas (post-orden) ──
    def expr(self, n):
        if n.kind == 'number':
            return 'float' if '.' in n.value else 'int'
        if n.kind == 'string':
            return 'string'
        if n.kind == 'boolean':
            return 'bool'
        if n.kind == 'new':
            return 'ptr'
        if n.kind == 'variable':
            return self.lookup(n.value, n)
        if n.kind == 'not':
            inner = self.expr(n.children[0])
            if inner != 'bool':
                self.error(n, f'El operador ! requiere bool, llegó {inner}')
            return 'bool'
        if n.kind == 'binary':
            a, b = (self.expr(c) for c in n.children)
            op = n.value
            if op in LOGICAL:
                if a != 'bool' or b != 'bool':
                    self.error(n, f'Operación {op} requiere bool, llegó {a} y {b}')
                return 'bool'
            if op in EQUALITY:
                # equivalencia de tipos, con la única coerción int↔float
                if a != b and not {a, b} <= NUMERIC:
                    self.error(n, 'Comparación de tipos incompatibles')
                return 'bool'
            if op in RELATIONAL:
                # Orden solo entre números: "hola" < "chao" sería válido en Python
                # pero en C compararía PUNTEROS; se prohíbe para que ambos backends coincidan.
                if a not in NUMERIC or b not in NUMERIC:
                    self.error(n, f'Comparación {op} solo entre números, llegó {a} y {b}')
                return 'bool'
            if a not in NUMERIC or b not in NUMERIC:
                self.error(n, f'Operación {op} inválida entre {a} y {b}')
            right = n.children[1]
            if op == '/' and right.kind == 'number' and float(right.value) == 0:
                # Solo se detecta el divisor LITERAL 0. "x / y" con y == 0 sigue
                # siendo un error de EJECUCIÓN: el valor de y no se conoce al compilar.
                self.error(n, 'División por cero (divisor constante 0)')
            # Coerción implícita (S6): int op float → float. Y '/' siempre es real:
            # 7 / 2 = 3.5 (decisión de diseño del lenguaje, no de Python).
            return 'float' if 'float' in (a, b) or op == '/' else 'int'
        raise ValueError(n.kind)

    def check(self, root):
        # Pasada 1: registrar TODAS las funciones antes de revisar cuerpos.
        # Así una llamada puede aparecer antes de la definición (declaración adelantada).
        for stmt in root.children:
            if stmt.kind == 'function':
                if stmt.value in self.functions:
                    self.error(stmt, f'Función duplicada: {stmt.value}')
                self.functions[stmt.value] = stmt
        # Pasada 2: revisar sentencias en orden textual.
        for stmt in root.children:
            if stmt.kind == 'function':
                self.scopes.append({})                 # enter_scope()
                self.block(stmt.children, stmt.value)
                self.scopes.pop()                      # exit_scope()
            else:
                self.block((stmt,), 'global')
        return self.symbols

    def compatible(self, expected, actual):
        """¿Se puede guardar `actual` en una variable `expected`?
        int → float se acepta (coerción segura, no pierde información);
        float → int NO (truncaría). ptr se guarda en int: es el "puntero didáctico"."""
        if expected == 'int' and actual == 'ptr':
            return True
        return expected == actual or (expected == 'float' and actual == 'int')

    def block(self, statements, scope):
        in_function = scope != 'global'
        for s in statements:
            if s.kind == 'declare':
                name, typ = s.value['name'], s.value['type']
                found = self.expr(s.children[0])       # el inicializador se revisa ANTES de declarar:
                if name in self.scopes[-1]:            # "int x = x;" falla por x no declarada
                    self.error(s, f'Declaración duplicada: {name}')
                if not self.compatible(typ, found):
                    self.error(s, f'{name}: se esperaba {typ}, llegó {found}')
                # Redeclarar SOLO se mira en scopes[-1]: un local puede tapar a un
                # global con el mismo nombre (shadowing), como en C.
                self.scopes[-1][name] = typ
                self.symbols.append({'name': name, 'type': typ, 'scope': scope,
                                     'line': s.line, 'column': s.column})
            elif s.kind == 'assign':
                expected = self.lookup(s.value, s)
                if in_function and s.value not in self.scopes[-1]:
                    # Las funciones no tienen paso por referencia ni globals mutables
                    # en esta versión: escribir un global desde una función se perdería
                    # al volver (cada marco tiene su copia). Se rechaza explícitamente.
                    self.error(s, f'{s.value} es global: una función solo puede leerla, no modificarla')
                actual = self.expr(s.children[0])
                if not self.compatible(expected, actual):
                    self.error(s, f'{s.value}: se esperaba {expected}, llegó {actual}')
            elif s.kind == 'print':
                self.expr(s.children[0])
            elif s.kind == 'return':
                if not in_function:
                    self.error(s, 'return fuera de una función')
                self.expr(s.children[0])
            elif s.kind == 'free':
                self.lookup(s.value, s)
            elif s.kind == 'call':
                if s.value not in self.functions:
                    self.error(s, f'Función {s.value} no declarada')
            elif s.kind == 'function':
                self.error(s, 'No se permiten funciones anidadas')


# ════════════════════════════════════════════════════════════════════════════
#  FASE 4 · REPRESENTACIÓN INTERMEDIA — [S7] TAC en cuádruplas
# ════════════════════════════════════════════════════════════════════════════

@dataclass
class Quad:
    """Cuádrupla (operador, arg1, arg2, resultado).

    Para BIN el campo b guarda (operador, arg2): el "op" de la cuádrupla es la
    clase de instrucción y el operador aritmético viaja junto al segundo operando.
    """
    op: str
    a: object = None
    b: object = None
    dest: object = None
    line: int = 0

    def show(self):
        if self.op == 'CONST': return f'{self.dest} = {self.a!r}'
        if self.op == 'MOV':   return f'{self.dest} = {self.a}'
        if self.op == 'BIN':   return f'{self.dest} = {self.a} {self.b[0]} {self.b[1]}'
        if self.op == 'PRINT': return f'print {self.a}'
        if self.op == 'ALLOC': return f'{self.dest} = alloc {self.a}'
        if self.op == 'FREE':  return f'free {self.a}'
        if self.op == 'ENTER': return f'enter {self.a}'
        if self.op == 'LEAVE': return f'leave {self.a}'
        if self.op == 'CALL':  return f'call {self.a}'
        if self.op == 'RET':   return f'return {self.a}'
        return str(self)


TEMP = re.compile(r't\d+')


def is_temp(name):
    """Temporales del compilador (t1, t2...) vs variables del usuario.
    Los usuarios no pueden "chocar" con ellos de forma peligrosa porque los
    temporales nunca aparecen como destino de un MOV escrito por el usuario."""
    return isinstance(name, str) and TEMP.fullmatch(name) is not None


class IRBuilder:
    """Aplana (linealiza) el AST: árbol 2D → cinta 1D de instrucciones atómicas.

    (?) ¿Dónde quedó la precedencia? En el ORDEN de emisión: expr() visita los
        hijos antes de emitir al padre (post-orden), así b*c se emite antes que a+t1.
    (?) ¿Por qué tantos temporales? El TAC supone registros INFINITOS; reducirlos a
        R0..R2 es problema del back-end (S10), no de esta fase.
    """

    def __init__(self):
        self.quads = []
        self.index = 0

    def emit(self, *args):
        self.quads.append(Quad(*args))

    def tmp(self):
        # Contador único en TODO el programa: cada temporal se asigna una sola vez
        # (parecido a SSA para temporales). El optimizador se apoya en esa garantía.
        self.index += 1
        return f't{self.index}'

    def expr(self, n):
        if n.kind in ('number', 'string', 'boolean'):
            t = self.tmp()
            if n.kind == 'number':
                v = float(n.value) if '.' in n.value else int(n.value)
            else:
                v = n.value
            self.emit('CONST', v, None, t, n.line)
            return t
        if n.kind == 'variable':
            return n.value                         # una variable ya es una "dirección": no gasta temporal
        if n.kind == 'new':
            t = self.tmp()
            self.emit('ALLOC', n.value, None, t, n.line)
            return t
        if n.kind == 'not':
            # !x  ≡  x == false : se reutiliza la comparación, sin opcode nuevo
            inner = self.expr(n.children[0])
            false_t = self.tmp()
            self.emit('CONST', False, None, false_t, n.line)
            t = self.tmp()
            self.emit('BIN', inner, ('==', false_t), t, n.line)
            return t
        if n.kind == 'binary':
            left = self.expr(n.children[0])
            right = self.expr(n.children[1])
            t = self.tmp()
            self.emit('BIN', left, (n.value, right), t, n.line)
            return t
        raise ValueError(n.kind)

    def statement(self, s):
        if s.kind in ('declare', 'assign'):
            dst = s.value['name'] if s.kind == 'declare' else s.value
            src = self.expr(s.children[0])
            self.emit('MOV', src, None, dst, s.line)
        elif s.kind == 'print':
            self.emit('PRINT', self.expr(s.children[0]), None, None, s.line)
        elif s.kind == 'free':
            self.emit('FREE', s.value, None, None, s.line)
        elif s.kind == 'call':
            self.emit('CALL', s.value, None, None, s.line)
        elif s.kind == 'return':
            self.emit('RET', self.expr(s.children[0]), None, None, s.line)

    def build(self, root):
        # Disposición de la "cinta": primero main (todo lo que no es función),
        # luego cada función entre ENTER/LEAVE. ENTER funciona como etiqueta de salto.
        funcs = {s.value: s for s in root.children if s.kind == 'function'}
        self.emit('ENTER', 'main', None, None, 1)
        for s in root.children:
            if s.kind != 'function':
                self.statement(s)
        self.emit('LEAVE', 'main', None, None, root.line)
        for name, fn in funcs.items():
            self.emit('ENTER', name, None, None, fn.line)
            for s in fn.children:
                self.statement(s)
            self.emit('LEAVE', name, None, None, fn.line)
        return self.quads


def format_value(v):
    """Cómo se IMPRIME un valor. Los bool salen como en el lenguaje fuente (true/false),
    no como Python (True/False): la salida debe depender del lenguaje, no del
    lenguaje en que está escrito el compilador. La comparten intérprete y CPU."""
    if isinstance(v, bool):
        return 'true' if v else 'false'
    return str(v)


def calculate(op, a, b):
    """Semántica de cada operador. La comparten el intérprete TAC y la CPU virtual:
    si ambos usan la misma definición, comparar sus salidas valida la TRADUCCIÓN."""
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/':
        if b == 0:
            raise ZeroDivisionError('Ejecución: división por cero')
        return a / b
    if op == '&&': return a and b
    if op == '||': return a or b
    return {'==': lambda: a == b, '!=': lambda: a != b, '<': lambda: a < b,
            '>': lambda: a > b, '<=': lambda: a <= b, '>=': lambda: a >= b}[op]()


# ════════════════════════════════════════════════════════════════════════════
#  FASE 5 · OPTIMIZACIÓN — [S9] mismo resultado observable, menos trabajo
# ════════════════════════════════════════════════════════════════════════════
#  Tres pasadas en orden:  algebraica → propagación + plegado → código muerto
#  Todas son LOCALES (recorren la lista de arriba a abajo). Funcionan porque el
#  lenguaje no tiene saltos: el programa entero de cada función es un único
#  bloque básico. Con if/while haría falta un grafo de flujo (CFG).

def simplify_algebraic(quads):
    """Identidades algebraicas y reducción de fuerza, aunque el otro operando NO sea constante.

        x + 0, 0 + x, x - 0  →  x          x * 1, 1 * x  →  x
        x * 2, 2 * x         →  x + x      (reducción de fuerza: sumar es más barato que multiplicar)

    Solo con constantes ENTERAS: x + 0.0 convertiría un int en float y cambiaría lo
    que se imprime (5 vs 5.0). Tampoco x * 0 → 0: si x fuera float el resultado sería 0.0.
    (?) ¿Por qué no x / 1 → x? Porque '/' en este lenguaje siempre da float.
    """
    consts = {q.dest: q.a for q in quads if q.op == 'CONST'}

    def is_int(name, value):
        v = consts.get(name)
        return type(v) is int and v == value       # type() estricto: True no cuenta como 1

    out, notes = [], []
    for q in quads:
        if q.op == 'BIN':
            op, right = q.b
            new = None
            if op in ('+', '-') and is_int(right, 0):
                new = Quad('MOV', q.a, None, q.dest, q.line); rule = f'x {op} 0 = x'
            elif op == '+' and is_int(q.a, 0):
                new = Quad('MOV', right, None, q.dest, q.line); rule = '0 + x = x'
            elif op == '*' and is_int(right, 1):
                new = Quad('MOV', q.a, None, q.dest, q.line); rule = 'x * 1 = x'
            elif op == '*' and is_int(q.a, 1):
                new = Quad('MOV', right, None, q.dest, q.line); rule = '1 * x = x'
            elif op == '*' and is_int(right, 2) and not is_temp_const(q.a, consts):
                new = Quad('BIN', q.a, ('+', q.a), q.dest, q.line); rule = 'x * 2 = x + x'
            elif op == '*' and is_int(q.a, 2) and not is_temp_const(right, consts):
                new = Quad('BIN', right, ('+', right), q.dest, q.line); rule = '2 * x = x + x'
            if new:
                notes.append(f'Línea {q.line}: simplificación algebraica ({rule}) en {q.dest}')
                q = new
        out.append(q)
    return out, notes


def is_temp_const(name, consts):
    # Si ambos lados son constantes, mejor dejar que el plegado calcule el valor final.
    return name in consts


def eliminate_dead_temporaries(quads):
    """DCE conservador: borra definiciones de temporales tN que nadie lee.

    Recorre AL REVÉS (de abajo hacia arriba) manteniendo el conjunto `live` de
    nombres que se usarán más adelante: es un análisis de vida (liveness) hacia atrás.
    No toca variables del usuario, PRINT, CALL ni operaciones de memoria (efectos laterales).
    """
    live, kept, notes = set(), [], []
    for q in reversed(quads):
        if q.op in ('CONST', 'MOV', 'BIN') and is_temp(q.dest) and q.dest not in live:
            notes.append(f'Línea {q.line}: temporal muerto {q.dest} eliminado')
            continue
        if q.dest is not None and q.op in ('CONST', 'MOV', 'BIN', 'ALLOC'):
            live.discard(q.dest)                  # antes de esta definición, el valor viejo no importa
        if q.op == 'BIN':
            live.add(q.a); live.add(q.b[1])
        elif q.op in ('MOV', 'PRINT', 'FREE', 'RET') and isinstance(q.a, str):
            live.add(q.a)
        kept.append(q)
    return list(reversed(kept)), list(reversed(notes))


def optimize(quads):
    """Pipeline de optimización. Devuelve (quads_optimizados, notas_explicativas)."""
    quads, notes = simplify_algebraic(quads)

    # Propagación + plegado de constantes. `known` = qué nombres valen una constante
    # conocida EN ESTE PUNTO del programa. Se vacía al cruzar ENTER/CALL/LEAVE porque
    # una llamada es una "caja negra" para un análisis local.
    known, out = {}, []
    for q in quads:
        if q.op == 'ENTER':
            known = {}
        if q.op == 'CONST':
            known[q.dest] = q.a
        elif q.op == 'MOV':
            if q.a in known:
                value = known[q.a]
                q = Quad('CONST', value, None, q.dest, q.line)
                known[q.dest] = value
                notes.append(f'Línea {q.line}: propagación de constante a {q.dest}')
            else:
                known.pop(q.dest, None)            # se reasignó con algo desconocido: deja de ser constante
        elif q.op == 'BIN':
            op, right = q.b
            if q.a in known and right in known:
                try:
                    v = calculate(op, known[q.a], known[right])
                    q = Quad('CONST', v, None, q.dest, q.line)
                    known[q.dest] = v
                    notes.append(f'Línea {q.line}: plegado constante en {q.dest}')
                except ZeroDivisionError:
                    # No se "pliega" un error: se deja la instrucción para que
                    # falle en ejecución exactamente como lo haría sin optimizar.
                    known.pop(q.dest, None)
            else:
                known.pop(q.dest, None)
        elif q.op in ('CALL', 'LEAVE'):
            known = {}
        out.append(q)

    # DCE solo sin llamadas: dentro de una función se podría leer un global cuyo
    # valor se calculó en main, y este análisis lineal no "ve" a través del CALL.
    if not any(q.op in ('CALL', 'RET') for q in out):
        out, dead_notes = eliminate_dead_temporaries(out)
        notes.extend(dead_notes)
    return out, notes


# ════════════════════════════════════════════════════════════════════════════
#  MEMORIA EN EJECUCIÓN — [S8] Stack de marcos (LIFO) y Heap
# ════════════════════════════════════════════════════════════════════════════

class Memory:
    """Modelo lógico, no byte a byte: la pila es una lista de marcos y el heap un
    dict dirección → tamaño. Lo comparten el intérprete TAC y la CPU virtual."""

    def __init__(self):
        self.stack = []
        self.heap = {}
        self.next_addr = 0x1000          # bump allocator: nunca reutiliza direcciones liberadas
        self.events = []

    def push(self, name):
        self.stack.append({'function': name, 'locals': {}})
        self.events.append(f'PUSH frame {name}')

    def pop(self):
        if not self.stack:
            raise RuntimeError('Stack underflow')
        name = self.stack.pop()['function']   # al salir, los locales se destruyen solos (gestión automática)
        self.events.append(f'POP frame {name}')

    def alloc(self, size):
        addr = self.next_addr
        self.next_addr += size
        self.heap[addr] = size
        self.events.append(f'HEAP ALLOC {size} bytes en {hex(addr)}')
        return addr                      # el "ticket del estacionamiento" (S8)

    def free(self, addr):
        # Como el allocator nunca reutiliza direcciones, un segundo free de la misma
        # dirección SIEMPRE se detecta (en malloc real podría pasar desapercibido).
        if addr not in self.heap:
            raise RuntimeError(f'Doble free o puntero inválido: {hex(addr)}')
        del self.heap[addr]
        self.events.append(f'HEAP FREE {hex(addr)}')


# ════════════════════════════════════════════════════════════════════════════
#  FASE 6 · GENERACIÓN DE CÓDIGO OBJETIVO — [S10] selección, registros y spill
# ════════════════════════════════════════════════════════════════════════════

OPCODES = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV',
           '==': 'EQ', '!=': 'NE', '<': 'LT', '>': 'GT', '<=': 'LE', '>=': 'GE',
           '&&': 'AND', '||': 'OR'}


class Backend:
    """TAC → ensamblador de una ISA virtual de 3 operandos (estilo RISC: OP dest, src1, src2).

    Estado del asignador:
        owners    registro → nombre que lo ocupa       (R0 → 't3')
        locations nombre   → registro donde está       ('t3' → R0)   (mapa inverso)
        slots     nombre   → dirección RAM de su spill ('a' → 0x2000)

    (?) ¿Qué algoritmo usan? Asignación LOCAL a demanda (S10 "Naive/Local"), no
        coloreado de grafos. La víctima del spill es la de MENOS usos futuros:
        heurística barata; la óptima teórica (Belady) sería "la que se usa más tarde".
    (?) ¿Por qué mínimo 3 registros? Una instrucción BIN necesita a la vez dos
        operandos y un destino; con 2 registros no hay donde poner el tercero.
    """

    def __init__(self, registers=3):
        if registers < 3:
            raise ValueError('Se requieren al menos 3 registros para esta ISA de tres operandos')
        self.regs = [f'R{i}' for i in range(registers)]
        self.owners = {}
        self.locations = {}
        self.asm = []
        self.events = []
        self.spills = 0
        self.slots = {}
        self.slot = 0

    def emit(self, s):
        self.asm.append(s)

    def uses(self, q):
        """Nombres que la cuádrupla LEE (no los que escribe)."""
        if q.op == 'BIN': return [q.a, q.b[1]]
        if q.op in ('MOV', 'PRINT', 'FREE', 'RET'): return [q.a]
        return []

    def future(self, quads, i):
        # Liveness APROXIMADO: cuenta lecturas en todo lo que queda de la cinta.
        # Sin saltos, "aparece más abajo" ≈ "está vivo". Con bucles esto dejaría de valer.
        return Counter(x for q in quads[i + 1:] for x in self.uses(q) if isinstance(x, str))

    def slot_for(self, name):
        if name not in self.slots:
            self.slots[name] = 0x2000 + self.slot * 8      # slots de 8 bytes en la zona de spill
            self.slot += 1
        return self.slots[name]

    def reg(self, name, quads, i, protect=()):
        """Devuelve el registro donde vive `name`, cargándolo o haciendo spill si hace falta.

        protect = nombres que NO pueden ser víctimas porque la instrucción actual
        los está usando (expulsar el operando izquierdo para cargar el derecho
        dejaría la instrucción sin uno de sus operandos).
        """
        if name in self.locations:
            return self.locations[name]
        free = next((r for r in self.regs if r not in self.owners), None)
        if free is None:
            # ── SPILL: no hay registros libres (S10, los 5 pasos) ──
            counts = self.future(quads, i)
            candidates = [(counts.get(v, 0), r, v) for r, v in self.owners.items() if v not in protect]
            if not candidates:
                raise RuntimeError('No hay registro libre para los operandos; aumente el pool')
            _, free, victim = min(candidates)              # 2. elegir víctima (menos usos futuros)
            if counts.get(victim, 0):                       # solo se guarda si alguien la volverá a leer:
                addr = self.slot_for(victim)                # un valor muerto se descarta sin STORE
                self.emit(f'STORE [{hex(addr)}], {free} ; SPILL {victim}')          # 3. STORE a RAM
                self.events.append(f'SPILL {victim}: {free} → STACK[{hex(addr)}]')
                self.spills += 1
            self.locations.pop(victim, None)
            self.owners.pop(free)
        self.owners[free] = name                            # 4. el registro queda para la nueva variable
        self.locations[name] = free
        if name in self.slots:                              # 5. si vivía en RAM, LOAD de vuelta
            self.emit(f'LOAD {free}, [{hex(self.slots[name])}] ; RECARGA {name}')
            self.events.append(f'RELOAD {name}: STACK → {free}')
        return free

    def release_dead(self, quads, i):
        # Tras cada instrucción, los registros de valores sin usos futuros quedan
        # libres: así 3 registros alcanzan para expresiones largas (reutilización).
        future = self.future(quads, i)
        for reg, name in list(self.owners.items()):
            if not future.get(name, 0):
                self.owners.pop(reg)
                self.locations.pop(name, None)

    def generate(self, quads):
        for i, q in enumerate(quads):
            if q.op in ('ENTER', 'LEAVE', 'CALL'):
                if q.op == 'CALL':
                    # Convención "caller-saved": la función llamada puede usar
                    # cualquier registro, así que el llamador guarda en RAM lo que
                    # aún necesita ANTES del salto. Al volver se recarga vía slots.
                    future = self.future(quads, i)
                    for register, name in list(self.owners.items()):
                        if future.get(name, 0):
                            addr = self.slot_for(name)
                            self.emit(f'STORE [{hex(addr)}], {register} ; CONSERVAR {name} ANTES DE CALL')
                            self.events.append(f'CALL-SAVE {name}: {register} → STACK[{hex(addr)}]')
                self.emit(f'{q.op} {q.a}')
                self.owners.clear()
                self.locations.clear()           # tras cruzar un límite de función, ningún registro es confiable
            elif q.op == 'CONST':
                r = self.reg(q.dest, quads, i)
                self.emit(f'LI {r}, {q.a!r} ; {q.dest}')          # LI = load immediate
            elif q.op == 'MOV':
                source = self.reg(q.a, quads, i)
                dest = self.reg(q.dest, quads, i, protect=(q.a,))
                self.emit(f'MOV {dest}, {source} ; {q.dest}')
            elif q.op == 'BIN':
                op, right = q.b
                leftreg = self.reg(q.a, quads, i)
                rightreg = self.reg(right, quads, i, protect=(q.a,))
                dest = self.reg(q.dest, quads, i, protect=(q.a, right))
                # Selección de instrucciones: aquí es 1 a 1 (cada operador TAC tiene
                # su opcode). En x86 real, "t1 = a + b" podría ser MOV+ADD o un LEA.
                self.emit(f'{OPCODES[op]} {dest}, {leftreg}, {rightreg} ; {q.dest}')
            elif q.op == 'PRINT':
                self.emit(f'PRINT {self.reg(q.a, quads, i)}')
            elif q.op == 'ALLOC':
                self.emit(f'ALLOC {self.reg(q.dest, quads, i)}, {q.a}')
            elif q.op == 'FREE':
                self.emit(f'FREE {self.reg(q.a, quads, i)}')
            elif q.op == 'RET':
                self.emit(f'RET {self.reg(q.a, quads, i)}')
            self.release_dead(quads, i)
        return self.asm


# ════════════════════════════════════════════════════════════════════════════
#  INTÉRPRETE DE TAC — "oráculo" contra el cual se valida la CPU virtual
# ════════════════════════════════════════════════════════════════════════════

class Interpreter:
    """Ejecuta las cuádruplas directamente (como el EmuladorVirtualIR de la S7).

    No sabe nada de registros ni de spill. Si su salida coincide con la de la CPU
    virtual, el back-end preservó la semántica (S10, reto 1 del back-end).
    """

    def __init__(self, quads):
        self.qs = quads
        self.memory = Memory()
        self.output = []
        self.globals = {}
        self.locals = {}
        self.calls = {}
        self.return_value = None

    def val(self, k):
        if k in self.locals: return self.locals[k]      # mismo orden de búsqueda que Semantic.lookup:
        if k in self.globals: return self.globals[k]    # primero el marco actual, luego el global
        raise RuntimeError(f'Variable temporal no inicializada: {k}')

    def execute(self):
        entries = {q.a: i for i, q in enumerate(self.qs) if q.op == 'ENTER'}
        self.memory.push('main')
        self.locals = {}
        pc = entries['main'] + 1
        steps = 0
        while pc < len(self.qs):
            steps += 1
            if steps > 10000:
                # Sin esto, una recursión f() { f(); } colgaría la GUI: es el "stack overflow" del simulador.
                raise RuntimeError('Límite de ejecución alcanzado')
            q = self.qs[pc]
            op = q.op
            if op == 'CONST':
                self.locals[q.dest] = q.a
            elif op == 'MOV':
                v = self.val(q.a)
                self.locals[q.dest] = v
                if not is_temp(q.dest):
                    if len(self.memory.stack) == 1:
                        self.globals[q.dest] = v
                    self.memory.stack[-1]['locals'][q.dest] = v
            elif op == 'BIN':
                self.locals[q.dest] = calculate(q.b[0], self.val(q.a), self.val(q.b[1]))
            elif op == 'PRINT':
                self.output.append(format_value(self.val(q.a)))
            elif op == 'ALLOC':
                self.locals[q.dest] = self.memory.alloc(q.a)
            elif op == 'FREE':
                self.memory.free(self.val(q.a))
            elif op == 'CALL':
                if q.a not in entries:
                    raise RuntimeError(f'Función no encontrada: {q.a}')
                # Dirección de retorno + entorno del llamador: lo que un stack frame real guarda.
                self.calls[len(self.memory.stack)] = (pc + 1, self.locals)
                self.memory.push(q.a)
                self.locals = {}
                pc = entries[q.a] + 1
                continue
            elif op in ('LEAVE', 'RET'):
                if op == 'RET':
                    self.return_value = self.val(q.a)
                self.memory.pop()
                if not self.memory.stack:
                    break                                  # se terminó main
                pc, self.locals = self.calls.pop(len(self.memory.stack))
                continue
            pc += 1
        return self.output


# ════════════════════════════════════════════════════════════════════════════
#  ORQUESTADOR — conecta las fases y devuelve todo lo que la GUI muestra
# ════════════════════════════════════════════════════════════════════════════

def compile_source(source, registers=3, optimized=False, run=True):
    """Ejecuta el pipeline completo. Nunca lanza excepciones hacia la GUI: cualquier
    error queda en result['error'] (S10, checklist: "sin detener abruptamente")."""
    result = {'source': source, 'error': None, 'error_phase': None}
    try:
        ts = lex(source)
        result['tokens'] = [asdict(t) for t in ts]
        from automata import analyze_automata, GRAMMAR   # import tardío: automata no depende de compiler
        result['automata'] = analyze_automata(ts)
        result['grammar'] = GRAMMAR

        ast = Parser(ts).parse()
        result['ast'] = ast.json()

        semantic = Semantic()
        result['symbols'] = semantic.check(ast)

        raw = IRBuilder().build(ast)
        result['tac'] = [q.show() for q in raw]
        # Se optimiza una COPIA para poder mostrar lado a lado TAC original vs optimizado.
        opt, notes = optimize([Quad(**asdict(q)) for q in raw])
        result['optimized_tac'] = [q.show() for q in opt]
        result['optimizations'] = notes

        chosen = opt if optimized else raw
        result['quads'] = [asdict(q) for q in chosen]
        backend = Backend(registers)
        result['assembly'] = backend.generate(chosen)
        result['register_events'] = backend.events
        result['spill_count'] = backend.spills
        result['register_slots'] = {name: hex(addr) for name, addr in backend.slots.items()}

        if run:
            vm = Interpreter(chosen)
            result['output'] = vm.execute()
            result['memory_events'] = vm.memory.events
            result['globals'] = vm.globals
            result['heap_remaining'] = vm.memory.heap

            from virtual_cpu import VirtualCPU             # import tardío: virtual_cpu importa compiler
            cpu = VirtualCPU(result['assembly'], registers)
            result['cpu_output'] = cpu.execute()
            result['cpu_trace'] = cpu.trace
            result['cpu_registers'] = cpu.registers
            result['cpu_ram'] = {hex(k): v for k, v in cpu.ram.items()}
            result['cpu_memory_events'] = cpu.memory.events
            result['cpu_heap_remaining'] = {hex(k): v for k, v in cpu.memory.heap.items()}
            # Validación cruzada: dos ejecuciones independientes (TAC vs ensamblador)
            # deben imprimir lo mismo; si no, el bug está en el back-end.
            result['cpu_matches_tac'] = (result['cpu_output'] == result['output'])
            if not result['cpu_matches_tac']:
                raise RuntimeError(f'Diferencia entre TAC {result["output"]} y CPU {result["cpu_output"]}')
        result['success'] = True
    except CompileError as e:
        result['success'] = False
        result['error'] = str(e)
        result['error_phase'] = e.phase
    except (RuntimeError, ZeroDivisionError, TypeError, ValueError) as e:
        # Lo que pasa DESPUÉS de compilar (doble free, división por cero con
        # variables, límite de pasos) es un error de ejecución, no de compilación.
        result['success'] = False
        result['error'] = str(e)
        result['error_phase'] = 'Ejecución'
    return result
