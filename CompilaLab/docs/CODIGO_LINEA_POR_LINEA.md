# CompilaLab — Guía de lectura línea por línea

Cada entrada conserva el número real de línea del archivo.
Las explicaciones son ayudas de lectura; las decisiones del algoritmo se estudian también con los tests.

## `compiler.py`

**Línea 1:** `"""CompilaLab: compilador educativo para una CPU virtual de pocos registros.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 3:** `Pipeline (S1, "Las 6 fases en acción"):`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 5:** `    texto ─► lex() ─► Parser ─► Semantic ─► IRBuilder ─► optimize() ─► Backend ─► VirtualCPU`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 6:** `            tokens     AST      tabla de     TAC /        TAC más       ISA         ejecución`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 7:** `                                símbolos     cuádruplas   pequeño       virtual     verificada`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 9:** `Front-end = lex + Parser + Semantic (depende del lenguaje fuente).`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 10:** `Middle-end = IRBuilder + optimize (independiente del lenguaje y de la máquina).`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 11:** `Back-end = Backend + VirtualCPU (depende de la "arquitectura" destino).`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 13:** `Convención de comentarios de estudio:`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 14:** `    [S#]  semana del curso donde se vio el concepto.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 15:** `    (?)   pregunta probable en la sustentación, con la idea clave para responderla.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 16:** `"""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 17:** `from __future__ import annotations`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 19:** `import re`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 20:** `from collections import Counter`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 21:** `from dataclasses import dataclass, asdict`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 24:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 25:** `#  ERRORES — [S1] "Clasificación de errores": cada fase lanza su propia categoría`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 26:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 28:** `class CompileError(Exception):`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 29:** `    """Error con fase + coordenadas. La fase le dice al programador QUÉ filtro falló."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 31:** `    def __init__(self, phase, line, column, message):`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 32:** `        super().__init__(f'{phase} (línea {line}, columna {column}): {message}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 33:** `        self.phase, self.line, self.column, self.message = phase, line, column, message`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 36:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 37:** `#  FASE 1 · ANÁLISIS LÉXICO — [S2] lexema / token / patrón`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 38:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 40:** `@dataclass`  
**Para qué sirve:** Genera automáticamente métodos para una clase de datos.  

**Línea 41:** `class Token:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 42:** `    kind: str     # token  = categoría que consume el parser (ID, NUMBER, '+', INT...)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 43:** `    value: str    # lexema = texto exacto leído del fuente`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 44:** `    line: int`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 45:** `    column: int`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 48:** `# Una sola regex maestra con named groups (?P<NOMBRE>...): el motor \`re\` prueba las`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 49:** `# alternativas DE IZQUIERDA A DERECHA, así que el orden es la tabla de prioridades:`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 50:** `#   · comentarios antes que el operador '/'      → "//" no se parte en dos '/'`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 51:** `#   · NUMBER acepta el decimal completo           → "3.14" no queda como 3 . 14   [S2 "FLOAT antes que INT"]`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 52:** `#   · STRING antes que UNCLOSED                   → solo cae en UNCLOSED si no hay comilla de cierre en la línea`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 53:** `#   · operadores de 2 caracteres antes que los de 1 → "<=" no se lee como '<' '='`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 54:** `#   · INVALID ('.') al final                     → atrapa cualquier carácter fuera del alfabeto`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 55:** `# Las palabras reservadas NO van en la regex: se reconoce un ID y luego se consulta`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 56:** `# KEYWORDS. Así "integer" no se corta en INT + "eger" (el problema que el \b resolvía en clase).`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 57:** `PATTERN = re.compile(`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 58:** `    r'(?P<COMMENT>//[^\n]*)'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 59:** `    r'&#124;(?P<BLOCK_COMMENT>/\*[\s\S]*?\*/)'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 60:** `    r'&#124;(?P<UNCLOSED_COMMENT>/\*)'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 61:** `    r'&#124;(?P<SPACE>[ \t\r]+)'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 62:** `    r'&#124;(?P<NEWLINE>\n)'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 63:** `    r'&#124;(?P<NUMBER>\d+(?:\.\d+)?)'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 64:** `    r'&#124;(?P<STRING>"(?:[^"\\\n]&#124;\\.)*")'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 65:** `    r'&#124;(?P<UNCLOSED>"[^"\n]*)'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 66:** `    r'&#124;(?P<ID>[a-zA-Z_]\w*)'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 67:** `    r'&#124;(?P<OP>==&#124;!=&#124;<=&#124;>=&#124;&&&#124;\&#124;\&#124;&#124;[+*/=;(){}<>,!-])'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 68:** `    r'&#124;(?P<INVALID>.)'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 69:** `)`  
**Para qué sirve:** Cierra una estructura o agrupación abierta previamente.  

**Línea 70:** `KEYWORDS = {'int', 'float', 'string', 'bool', 'true', 'false',`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 71:** `            'print', 'fn', 'return', 'new', 'free'}`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 74:** `def lex(source):`  
**Para qué sirve:** Define la función `lex` y sus parámetros de entrada.  

**Línea 75:** `    """Escanea de izquierda a derecha y devuelve la lista de tokens terminada en EOF.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 77:** `    Recuperación en "modo pánico" (S2, cláusula ERROR): un carácter inválido no`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 78:** `    detiene el escaneo; se anota y se sigue, para reportar TODOS los errores léxicos`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 79:** `    de una vez. Solo al final se lanza un único CompileError con el primero y el conteo.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 80:** `    """`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 81:** `    tokens, errors = [], []`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 82:** `    line, col = 1, 1`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 83:** `    for m in PATTERN.finditer(source):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 84:** `        kind, val = m.lastgroup, m.group()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 85:** `        if kind == 'NEWLINE':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 86:** `            line, col = line + 1, 1`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 87:** `            continue`  
**Para qué sirve:** Salta a la siguiente iteración del ciclo.  

**Línea 88:** `        if kind == 'BLOCK_COMMENT':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 89:** `            # Un comentario multilínea "consume" saltos de línea: si no se cuentan,`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 90:** `            # todas las coordenadas posteriores quedan corridas (reto de la S2).`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 91:** `            breaks = val.count('\n')`  
**Para qué sirve:** Termina el ciclo actual.  

**Línea 92:** `            if breaks:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 93:** `                line += breaks`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 94:** `                col = len(val) - val.rfind('\n')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 95:** `            else:`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 96:** `                col += len(val)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 97:** `            continue`  
**Para qué sirve:** Salta a la siguiente iteración del ciclo.  

**Línea 98:** `        if kind in ('SPACE', 'COMMENT'):          # ruido: se descarta, pero mueve la columna`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 99:** `            col += len(val)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 100:** `            continue`  
**Para qué sirve:** Salta a la siguiente iteración del ciclo.  

**Línea 101:** `        if kind == 'UNCLOSED':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 102:** `            errors.append((line, col, 'Cadena sin cerrar'))`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 103:** `        elif kind == 'UNCLOSED_COMMENT':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 104:** `            errors.append((line, col, 'Comentario /* sin cerrar'))`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 105:** `        elif kind == 'INVALID':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 106:** `            errors.append((line, col, f'Carácter inválido {val!r}'))`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 107:** `        else:`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 108:** `            if kind == 'ID' and val in KEYWORDS:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 109:** `                kind = val.upper()                # 'int' → token INT`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 110:** `            elif kind == 'OP':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 111:** `                kind = val                        # el propio símbolo es el tipo de token`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 112:** `            tokens.append(Token(kind, val, line, col))`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 113:** `        col += len(val)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 114:** `    if errors:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 115:** `        first_line, first_col, message = errors[0]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 116:** `        if len(errors) > 1:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 117:** `            rest = ', '.join(f'L{l}:C{c} {msg}' for l, c, msg in errors[1:4])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 118:** `            message += f' (+{len(errors) - 1} error(es) léxico(s) más: {rest})'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 119:** `        raise CompileError('Léxico', first_line, first_col, message)`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 120:** `    tokens.append(Token('EOF', '', line, col))   # centinela: el parser nunca se sale de la lista`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 121:** `    return tokens`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 124:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 125:** `#  FASE 2 · ANÁLISIS SINTÁCTICO — [S3-S4] gramática libre de contexto → AST`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 126:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 128:** `@dataclass`  
**Para qué sirve:** Genera automáticamente métodos para una clase de datos.  

**Línea 129:** `class Node:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 130:** `    """Nodo del AST. Es ABSTRACTO: no guarda ';', '(' ni ')' porque la forma del`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 131:** `    árbol ya codifica la agrupación (S4: árbol de parseo concreto vs AST)."""`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 132:** `    kind: str`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 133:** `    line: int`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 134:** `    value: object = None`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 135:** `    children: tuple = ()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 136:** `    column: int = 0`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 138:** `    def json(self):`  
**Para qué sirve:** Define la función `json` y sus parámetros de entrada.  

**Línea 139:** `        return {'kind': self.kind, 'line': self.line, 'column': self.column,`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 140:** `                'value': self.value, 'children': [c.json() for c in self.children]}`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 143:** `class Parser:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 144:** `    """Descenso recursivo (Top-Down, LL(1)): una función por no terminal.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 146:** `    Gramática completa en automata.GRAMMAR. La precedencia sale de la PROFUNDIDAD`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 147:** `    de las llamadas: la regla más "abajo" (mul) se reduce primero, así que`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 148:** `    a + b * c produce '+'(a, '*'(b, c)) sin tabla de precedencias.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 150:** `    (?) ¿Por qué no hay recursión infinita? Las reglas se escribieron en EBNF con`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 151:** `        repetición (X → Y (op Y)*) en vez de X → X op Y; un while reemplaza la`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 152:** `        recursión izquierda que colgaría a un parser Top-Down (S4).`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 153:** `    (?) ¿Y la asociatividad? El while va "acumulando" left = op(left, siguiente),`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 154:** `        por eso 10 - 3 - 2 es (10 - 3) - 2: asociatividad izquierda.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 155:** `    """`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 157:** `    def __init__(self, tokens):`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 158:** `        self.ts = tokens`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 159:** `        self.i = 0`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 161:** `    # ── utilidades: "mirar" sin consumir (lookahead de 1 token) y "consumir" ──`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 162:** `    def at(self, *kinds):`  
**Para qué sirve:** Define la función `at` y sus parámetros de entrada.  

**Línea 163:** `        return self.ts[self.i].kind in kinds`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 165:** `    def take(self, kind=None):`  
**Para qué sirve:** Define la función `take` y sus parámetros de entrada.  

**Línea 166:** `        t = self.ts[self.i]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 167:** `        if kind and t.kind != kind:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 168:** `            raise CompileError('Sintáctico', t.line, t.column,`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 169:** `                               f'Se esperaba {kind}, llegó {t.value or "fin de archivo"!r}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 170:** `        self.i += 1`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 171:** `        return t`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 173:** `    def node(self, kind, tok, value=None, children=()):`  
**Para qué sirve:** Define la función `node` y sus parámetros de entrada.  

**Línea 174:** `        return Node(kind, tok.line, value, tuple(children), tok.column)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 176:** `    # program → statement* EOF`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 177:** `    def parse(self):`  
**Para qué sirve:** Define la función `parse` y sus parámetros de entrada.  

**Línea 178:** `        items = []`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 179:** `        while not self.at('EOF'):`  
**Para qué sirve:** Repite un bloque mientras la condición siga siendo verdadera.  

**Línea 180:** `            items.append(self.statement())`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 181:** `        return Node('program', 1, children=tuple(items), column=1)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 183:** `    def statement(self):`  
**Para qué sirve:** Define la función `statement` y sus parámetros de entrada.  

**Línea 184:** `        # El PRIMER token decide la producción (conjunto FIRST): eso es lo que`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 185:** `        # hace a la gramática predictiva y evita backtracking.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 186:** `        t = self.ts[self.i]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 187:** `        if self.at('INT', 'FLOAT', 'STRING', 'BOOL'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 188:** `            typ = self.take().value`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 189:** `            name = self.take('ID')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 190:** `            self.take('=')`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 191:** `            exp = self.expr()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 192:** `            self.take(';')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 193:** `            return self.node('declare', name, {'type': typ, 'name': name.value}, (exp,))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 194:** `        if self.at('PRINT'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 195:** `            self.take(); self.take('(')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 196:** `            exp = self.expr()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 197:** `            self.take(')'); self.take(';')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 198:** `            return self.node('print', t, children=(exp,))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 199:** `        if self.at('FREE'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 200:** `            self.take(); self.take('(')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 201:** `            name = self.take('ID')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 202:** `            self.take(')'); self.take(';')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 203:** `            return self.node('free', name, name.value)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 204:** `        if self.at('FN'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 205:** `            self.take()`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 206:** `            name = self.take('ID')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 207:** `            self.take('('); self.take(')'); self.take('{')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 208:** `            body = []`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 209:** `            while not self.at('}', 'EOF'):`  
**Para qué sirve:** Repite un bloque mientras la condición siga siendo verdadera.  

**Línea 210:** `                body.append(self.statement())`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 211:** `            self.take('}')                      # si llegó EOF, aquí sale "Se esperaba }"`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 212:** `            return self.node('function', name, name.value, body)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 213:** `        if self.at('RETURN'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 214:** `            self.take()`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 215:** `            exp = self.expr()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 216:** `            self.take(';')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 217:** `            return self.node('return', t, children=(exp,))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 218:** `        if self.at('ID'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 219:** `            # ID es ambiguo con 1 token (llamada o asignación); el SEGUNDO token`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 220:** `            # desempata. Por eso se consume el ID y se mira lo que sigue.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 221:** `            name = self.take()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 222:** `            if self.at('('):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 223:** `                self.take('('); self.take(')'); self.take(';')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 224:** `                return self.node('call', name, name.value)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 225:** `            self.take('=')`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 226:** `            exp = self.expr()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 227:** `            self.take(';')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 228:** `            return self.node('assign', name, name.value, (exp,))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 229:** `        raise CompileError('Sintáctico', t.line, t.column, f'Sentencia inesperada {t.value!r}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 231:** `    # ── expresiones: de MENOR a MAYOR precedencia ──`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 232:** `    #   &#124;&#124;  <  &&  <  comparación  <  + -  <  * /  <  unario  <  átomo`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 233:** `    def expr(self):`  
**Para qué sirve:** Define la función `expr` y sus parámetros de entrada.  

**Línea 234:** `        return self.logic_or()`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 236:** `    def binary_level(self, operators, next_level):`  
**Para qué sirve:** Define la función `binary_level` y sus parámetros de entrada.  

**Línea 237:** `        """Plantilla común de los niveles  X → Y (op Y)*  (evita repetir 5 veces el while)."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 238:** `        left = next_level()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 239:** `        while self.at(*operators):`  
**Para qué sirve:** Repite un bloque mientras la condición siga siendo verdadera.  

**Línea 240:** `            op = self.take()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 241:** `            left = self.node('binary', op, op.value, (left, next_level()))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 242:** `        return left`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 244:** `    def logic_or(self):`  
**Para qué sirve:** Define la función `logic_or` y sus parámetros de entrada.  

**Línea 245:** `        return self.binary_level(('&#124;&#124;',), self.logic_and)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 247:** `    def logic_and(self):`  
**Para qué sirve:** Define la función `logic_and` y sus parámetros de entrada.  

**Línea 248:** `        return self.binary_level(('&&',), self.comparison)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 250:** `    def comparison(self):`  
**Para qué sirve:** Define la función `comparison` y sus parámetros de entrada.  

**Línea 251:** `        return self.binary_level(('==', '!=', '<', '>', '<=', '>='), self.add)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 253:** `    def add(self):`  
**Para qué sirve:** Define la función `add` y sus parámetros de entrada.  

**Línea 254:** `        return self.binary_level(('+', '-'), self.mul)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 256:** `    def mul(self):`  
**Para qué sirve:** Define la función `mul` y sus parámetros de entrada.  

**Línea 257:** `        return self.binary_level(('*', '/'), self.unary)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 259:** `    def unary(self):`  
**Para qué sirve:** Define la función `unary` y sus parámetros de entrada.  

**Línea 260:** `        if self.at('-'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 261:** `            # "Azúcar sintáctico": -x se reescribe como 0 - x. Así el resto del`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 262:** `            # compilador no necesita un operador unario aritmético.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 263:** `            t = self.take()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 264:** `            return self.node('binary', t, '-', (self.node('number', t, '0'), self.unary()))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 265:** `        if self.at('!'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 266:** `            t = self.take()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 267:** `            return self.node('not', t, children=(self.unary(),))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 268:** `        return self.atom()`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 270:** `    def atom(self):`  
**Para qué sirve:** Define la función `atom` y sus parámetros de entrada.  

**Línea 271:** `        t = self.ts[self.i]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 272:** `        if self.at('NUMBER'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 273:** `            self.take(); return self.node('number', t, t.value)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 274:** `        if self.at('STRING'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 275:** `            self.take(); return self.node('string', t, t.value[1:-1])   # se quitan las comillas`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 276:** `        if self.at('TRUE', 'FALSE'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 277:** `            self.take(); return self.node('boolean', t, t.value == 'true')`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 278:** `        if self.at('ID'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 279:** `            self.take(); return self.node('variable', t, t.value)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 280:** `        if self.at('NEW'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 281:** `            self.take(); self.take('(')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 282:** `            size = self.take('NUMBER')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 283:** `            self.take(')')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 284:** `            if '.' in size.value or int(size.value) <= 0:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 285:** `                raise CompileError('Sintáctico', size.line, size.column, 'new requiere un entero positivo')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 286:** `            return self.node('new', t, int(size.value))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 287:** `        if self.at('('):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 288:** `            # Los paréntesis desaparecen del AST: solo sirven para volver a empezar`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 289:** `            # desde la precedencia más baja (expr) dentro de un factor.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 290:** `            self.take()`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 291:** `            exp = self.expr()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 292:** `            self.take(')')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 293:** `            return exp`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 294:** `        raise CompileError('Sintáctico', t.line, t.column, f'Expresión inesperada {t.value!r}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 297:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 298:** `#  FASE 3 · ANÁLISIS SEMÁNTICO — [S5] tabla de símbolos y ámbitos, [S6] tipos`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 299:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 301:** `NUMERIC = {'int', 'float'}`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 302:** `RELATIONAL = ('<', '>', '<=', '>=')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 303:** `EQUALITY = ('==', '!=')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 304:** `LOGICAL = ('&&', '&#124;&#124;')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 307:** `class Semantic:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 308:** `    """Recorre el AST validando SIGNIFICADO: existencia, ámbito y tipos.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 310:** `    self.scopes es la PILA de ámbitos de la S5: [global, local_de_función].`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 311:** `    Entrar a una función = push de un dict vacío; salir = pop (sus variables "mueren").`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 312:** `    self.symbols es solo el registro histórico que se muestra en la GUI.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 313:** `    """`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 315:** `    def __init__(self):`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 316:** `        self.scopes = [{}]`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 317:** `        self.symbols = []`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 318:** `        self.functions = {}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 320:** `    def lookup(self, name, node):`  
**Para qué sirve:** Define la función `lookup` y sus parámetros de entrada.  

**Línea 321:** `        # Búsqueda léxica: del ámbito actual hacia el global (S5, "vidrio espía":`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 322:** `        # desde adentro se ve hacia afuera, nunca al revés).`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 323:** `        for scope in reversed(self.scopes):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 324:** `            if name in scope:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 325:** `                return scope[name]`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 326:** `        raise CompileError('Semántico', node.line, node.column, f'Variable {name!r} no declarada')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 328:** `    def error(self, node, message):`  
**Para qué sirve:** Define la función `error` y sus parámetros de entrada.  

**Línea 329:** `        raise CompileError('Semántico', node.line, node.column, message)`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 331:** `    # ── [S6] inferencia: cada expresión "sube" su tipo desde las hojas (post-orden) ──`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 332:** `    def expr(self, n):`  
**Para qué sirve:** Define la función `expr` y sus parámetros de entrada.  

**Línea 333:** `        if n.kind == 'number':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 334:** `            return 'float' if '.' in n.value else 'int'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 335:** `        if n.kind == 'string':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 336:** `            return 'string'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 337:** `        if n.kind == 'boolean':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 338:** `            return 'bool'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 339:** `        if n.kind == 'new':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 340:** `            return 'ptr'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 341:** `        if n.kind == 'variable':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 342:** `            return self.lookup(n.value, n)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 343:** `        if n.kind == 'not':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 344:** `            inner = self.expr(n.children[0])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 345:** `            if inner != 'bool':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 346:** `                self.error(n, f'El operador ! requiere bool, llegó {inner}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 347:** `            return 'bool'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 348:** `        if n.kind == 'binary':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 349:** `            a, b = (self.expr(c) for c in n.children)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 350:** `            op = n.value`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 351:** `            if op in LOGICAL:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 352:** `                if a != 'bool' or b != 'bool':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 353:** `                    self.error(n, f'Operación {op} requiere bool, llegó {a} y {b}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 354:** `                return 'bool'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 355:** `            if op in EQUALITY:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 356:** `                # equivalencia de tipos, con la única coerción int↔float`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 357:** `                if a != b and not {a, b} <= NUMERIC:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 358:** `                    self.error(n, 'Comparación de tipos incompatibles')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 359:** `                return 'bool'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 360:** `            if op in RELATIONAL:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 361:** `                # Orden solo entre números: "hola" < "chao" sería válido en Python`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 362:** `                # pero en C compararía PUNTEROS; se prohíbe para que ambos backends coincidan.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 363:** `                if a not in NUMERIC or b not in NUMERIC:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 364:** `                    self.error(n, f'Comparación {op} solo entre números, llegó {a} y {b}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 365:** `                return 'bool'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 366:** `            if a not in NUMERIC or b not in NUMERIC:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 367:** `                self.error(n, f'Operación {op} inválida entre {a} y {b}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 368:** `            right = n.children[1]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 369:** `            if op == '/' and right.kind == 'number' and float(right.value) == 0:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 370:** `                # Solo se detecta el divisor LITERAL 0. "x / y" con y == 0 sigue`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 371:** `                # siendo un error de EJECUCIÓN: el valor de y no se conoce al compilar.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 372:** `                self.error(n, 'División por cero (divisor constante 0)')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 373:** `            # Coerción implícita (S6): int op float → float. Y '/' siempre es real:`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 374:** `            # 7 / 2 = 3.5 (decisión de diseño del lenguaje, no de Python).`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 375:** `            return 'float' if 'float' in (a, b) or op == '/' else 'int'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 376:** `        raise ValueError(n.kind)`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 378:** `    def check(self, root):`  
**Para qué sirve:** Define la función `check` y sus parámetros de entrada.  

**Línea 379:** `        # Pasada 1: registrar TODAS las funciones antes de revisar cuerpos.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 380:** `        # Así una llamada puede aparecer antes de la definición (declaración adelantada).`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 381:** `        for stmt in root.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 382:** `            if stmt.kind == 'function':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 383:** `                if stmt.value in self.functions:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 384:** `                    self.error(stmt, f'Función duplicada: {stmt.value}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 385:** `                self.functions[stmt.value] = stmt`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 386:** `        # Pasada 2: revisar sentencias en orden textual.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 387:** `        for stmt in root.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 388:** `            if stmt.kind == 'function':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 389:** `                self.scopes.append({})                 # enter_scope()`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 390:** `                self.block(stmt.children, stmt.value)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 391:** `                self.scopes.pop()                      # exit_scope()`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 392:** `            else:`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 393:** `                self.block((stmt,), 'global')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 394:** `        return self.symbols`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 396:** `    def compatible(self, expected, actual):`  
**Para qué sirve:** Define la función `compatible` y sus parámetros de entrada.  

**Línea 397:** `        """¿Se puede guardar \`actual\` en una variable \`expected\`?`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 398:** `        int → float se acepta (coerción segura, no pierde información);`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 399:** `        float → int NO (truncaría). ptr se guarda en int: es el "puntero didáctico"."""`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 400:** `        if expected == 'int' and actual == 'ptr':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 401:** `            return True`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 402:** `        return expected == actual or (expected == 'float' and actual == 'int')`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 404:** `    def block(self, statements, scope):`  
**Para qué sirve:** Define la función `block` y sus parámetros de entrada.  

**Línea 405:** `        in_function = scope != 'global'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 406:** `        for s in statements:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 407:** `            if s.kind == 'declare':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 408:** `                name, typ = s.value['name'], s.value['type']`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 409:** `                found = self.expr(s.children[0])       # el inicializador se revisa ANTES de declarar:`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 410:** `                if name in self.scopes[-1]:            # "int x = x;" falla por x no declarada`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 411:** `                    self.error(s, f'Declaración duplicada: {name}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 412:** `                if not self.compatible(typ, found):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 413:** `                    self.error(s, f'{name}: se esperaba {typ}, llegó {found}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 414:** `                # Redeclarar SOLO se mira en scopes[-1]: un local puede tapar a un`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 415:** `                # global con el mismo nombre (shadowing), como en C.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 416:** `                self.scopes[-1][name] = typ`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 417:** `                self.symbols.append({'name': name, 'type': typ, 'scope': scope,`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 418:** `                                     'line': s.line, 'column': s.column})`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 419:** `            elif s.kind == 'assign':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 420:** `                expected = self.lookup(s.value, s)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 421:** `                if in_function and s.value not in self.scopes[-1]:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 422:** `                    # Las funciones no tienen paso por referencia ni globals mutables`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 423:** `                    # en esta versión: escribir un global desde una función se perdería`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 424:** `                    # al volver (cada marco tiene su copia). Se rechaza explícitamente.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 425:** `                    self.error(s, f'{s.value} es global: una función solo puede leerla, no modificarla')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 426:** `                actual = self.expr(s.children[0])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 427:** `                if not self.compatible(expected, actual):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 428:** `                    self.error(s, f'{s.value}: se esperaba {expected}, llegó {actual}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 429:** `            elif s.kind == 'print':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 430:** `                self.expr(s.children[0])`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 431:** `            elif s.kind == 'return':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 432:** `                if not in_function:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 433:** `                    self.error(s, 'return fuera de una función')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 434:** `                self.expr(s.children[0])`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 435:** `            elif s.kind == 'free':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 436:** `                self.lookup(s.value, s)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 437:** `            elif s.kind == 'call':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 438:** `                if s.value not in self.functions:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 439:** `                    self.error(s, f'Función {s.value} no declarada')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 440:** `            elif s.kind == 'function':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 441:** `                self.error(s, 'No se permiten funciones anidadas')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 444:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 445:** `#  FASE 4 · REPRESENTACIÓN INTERMEDIA — [S7] TAC en cuádruplas`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 446:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 448:** `@dataclass`  
**Para qué sirve:** Genera automáticamente métodos para una clase de datos.  

**Línea 449:** `class Quad:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 450:** `    """Cuádrupla (operador, arg1, arg2, resultado).`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 452:** `    Para BIN el campo b guarda (operador, arg2): el "op" de la cuádrupla es la`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 453:** `    clase de instrucción y el operador aritmético viaja junto al segundo operando.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 454:** `    """`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 455:** `    op: str`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 456:** `    a: object = None`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 457:** `    b: object = None`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 458:** `    dest: object = None`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 459:** `    line: int = 0`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 461:** `    def show(self):`  
**Para qué sirve:** Define la función `show` y sus parámetros de entrada.  

**Línea 462:** `        if self.op == 'CONST': return f'{self.dest} = {self.a!r}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 463:** `        if self.op == 'MOV':   return f'{self.dest} = {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 464:** `        if self.op == 'BIN':   return f'{self.dest} = {self.a} {self.b[0]} {self.b[1]}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 465:** `        if self.op == 'PRINT': return f'print {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 466:** `        if self.op == 'ALLOC': return f'{self.dest} = alloc {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 467:** `        if self.op == 'FREE':  return f'free {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 468:** `        if self.op == 'ENTER': return f'enter {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 469:** `        if self.op == 'LEAVE': return f'leave {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 470:** `        if self.op == 'CALL':  return f'call {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 471:** `        if self.op == 'RET':   return f'return {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 472:** `        return str(self)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 475:** `TEMP = re.compile(r't\d+')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 478:** `def is_temp(name):`  
**Para qué sirve:** Define la función `is_temp` y sus parámetros de entrada.  

**Línea 479:** `    """Temporales del compilador (t1, t2...) vs variables del usuario.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 480:** `    Los usuarios no pueden "chocar" con ellos de forma peligrosa porque los`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 481:** `    temporales nunca aparecen como destino de un MOV escrito por el usuario."""`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 482:** `    return isinstance(name, str) and TEMP.fullmatch(name) is not None`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 485:** `class IRBuilder:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 486:** `    """Aplana (linealiza) el AST: árbol 2D → cinta 1D de instrucciones atómicas.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 488:** `    (?) ¿Dónde quedó la precedencia? En el ORDEN de emisión: expr() visita los`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 489:** `        hijos antes de emitir al padre (post-orden), así b*c se emite antes que a+t1.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 490:** `    (?) ¿Por qué tantos temporales? El TAC supone registros INFINITOS; reducirlos a`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 491:** `        R0..R2 es problema del back-end (S10), no de esta fase.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 492:** `    """`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 494:** `    def __init__(self):`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 495:** `        self.quads = []`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 496:** `        self.index = 0`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 498:** `    def emit(self, *args):`  
**Para qué sirve:** Define la función `emit` y sus parámetros de entrada.  

**Línea 499:** `        self.quads.append(Quad(*args))`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 501:** `    def tmp(self):`  
**Para qué sirve:** Define la función `tmp` y sus parámetros de entrada.  

**Línea 502:** `        # Contador único en TODO el programa: cada temporal se asigna una sola vez`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 503:** `        # (parecido a SSA para temporales). El optimizador se apoya en esa garantía.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 504:** `        self.index += 1`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 505:** `        return f't{self.index}'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 507:** `    def expr(self, n):`  
**Para qué sirve:** Define la función `expr` y sus parámetros de entrada.  

**Línea 508:** `        if n.kind in ('number', 'string', 'boolean'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 509:** `            t = self.tmp()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 510:** `            if n.kind == 'number':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 511:** `                v = float(n.value) if '.' in n.value else int(n.value)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 512:** `            else:`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 513:** `                v = n.value`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 514:** `            self.emit('CONST', v, None, t, n.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 515:** `            return t`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 516:** `        if n.kind == 'variable':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 517:** `            return n.value                         # una variable ya es una "dirección": no gasta temporal`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 518:** `        if n.kind == 'new':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 519:** `            t = self.tmp()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 520:** `            self.emit('ALLOC', n.value, None, t, n.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 521:** `            return t`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 522:** `        if n.kind == 'not':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 523:** `            # !x  ≡  x == false : se reutiliza la comparación, sin opcode nuevo`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 524:** `            inner = self.expr(n.children[0])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 525:** `            false_t = self.tmp()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 526:** `            self.emit('CONST', False, None, false_t, n.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 527:** `            t = self.tmp()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 528:** `            self.emit('BIN', inner, ('==', false_t), t, n.line)`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 529:** `            return t`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 530:** `        if n.kind == 'binary':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 531:** `            left = self.expr(n.children[0])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 532:** `            right = self.expr(n.children[1])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 533:** `            t = self.tmp()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 534:** `            self.emit('BIN', left, (n.value, right), t, n.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 535:** `            return t`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 536:** `        raise ValueError(n.kind)`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 538:** `    def statement(self, s):`  
**Para qué sirve:** Define la función `statement` y sus parámetros de entrada.  

**Línea 539:** `        if s.kind in ('declare', 'assign'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 540:** `            dst = s.value['name'] if s.kind == 'declare' else s.value`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 541:** `            src = self.expr(s.children[0])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 542:** `            self.emit('MOV', src, None, dst, s.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 543:** `        elif s.kind == 'print':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 544:** `            self.emit('PRINT', self.expr(s.children[0]), None, None, s.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 545:** `        elif s.kind == 'free':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 546:** `            self.emit('FREE', s.value, None, None, s.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 547:** `        elif s.kind == 'call':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 548:** `            self.emit('CALL', s.value, None, None, s.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 549:** `        elif s.kind == 'return':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 550:** `            self.emit('RET', self.expr(s.children[0]), None, None, s.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 552:** `    def build(self, root):`  
**Para qué sirve:** Define la función `build` y sus parámetros de entrada.  

**Línea 553:** `        # Disposición de la "cinta": primero main (todo lo que no es función),`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 554:** `        # luego cada función entre ENTER/LEAVE. ENTER funciona como etiqueta de salto.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 555:** `        funcs = {s.value: s for s in root.children if s.kind == 'function'}`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 556:** `        self.emit('ENTER', 'main', None, None, 1)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 557:** `        for s in root.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 558:** `            if s.kind != 'function':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 559:** `                self.statement(s)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 560:** `        self.emit('LEAVE', 'main', None, None, root.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 561:** `        for name, fn in funcs.items():`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 562:** `            self.emit('ENTER', name, None, None, fn.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 563:** `            for s in fn.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 564:** `                self.statement(s)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 565:** `            self.emit('LEAVE', name, None, None, fn.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 566:** `        return self.quads`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 569:** `def format_value(v):`  
**Para qué sirve:** Define la función `format_value` y sus parámetros de entrada.  

**Línea 570:** `    """Cómo se IMPRIME un valor. Los bool salen como en el lenguaje fuente (true/false),`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 571:** `    no como Python (True/False): la salida debe depender del lenguaje, no del`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 572:** `    lenguaje en que está escrito el compilador. La comparten intérprete y CPU."""`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 573:** `    if isinstance(v, bool):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 574:** `        return 'true' if v else 'false'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 575:** `    return str(v)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 578:** `def calculate(op, a, b):`  
**Para qué sirve:** Define la función `calculate` y sus parámetros de entrada.  

**Línea 579:** `    """Semántica de cada operador. La comparten el intérprete TAC y la CPU virtual:`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 580:** `    si ambos usan la misma definición, comparar sus salidas valida la TRADUCCIÓN."""`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 581:** `    if op == '+': return a + b`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 582:** `    if op == '-': return a - b`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 583:** `    if op == '*': return a * b`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 584:** `    if op == '/':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 585:** `        if b == 0:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 586:** `            raise ZeroDivisionError('Ejecución: división por cero')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 587:** `        return a / b`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 588:** `    if op == '&&': return a and b`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 589:** `    if op == '&#124;&#124;': return a or b`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 590:** `    return {'==': lambda: a == b, '!=': lambda: a != b, '<': lambda: a < b,`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 591:** `            '>': lambda: a > b, '<=': lambda: a <= b, '>=': lambda: a >= b}[op]()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 594:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 595:** `#  FASE 5 · OPTIMIZACIÓN — [S9] mismo resultado observable, menos trabajo`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 596:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 597:** `#  Tres pasadas en orden:  algebraica → propagación + plegado → código muerto`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 598:** `#  Todas son LOCALES (recorren la lista de arriba a abajo). Funcionan porque el`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 599:** `#  lenguaje no tiene saltos: el programa entero de cada función es un único`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 600:** `#  bloque básico. Con if/while haría falta un grafo de flujo (CFG).`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 602:** `def simplify_algebraic(quads):`  
**Para qué sirve:** Define la función `simplify_algebraic` y sus parámetros de entrada.  

**Línea 603:** `    """Identidades algebraicas y reducción de fuerza, aunque el otro operando NO sea constante.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 605:** `        x + 0, 0 + x, x - 0  →  x          x * 1, 1 * x  →  x`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 606:** `        x * 2, 2 * x         →  x + x      (reducción de fuerza: sumar es más barato que multiplicar)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 608:** `    Solo con constantes ENTERAS: x + 0.0 convertiría un int en float y cambiaría lo`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 609:** `    que se imprime (5 vs 5.0). Tampoco x * 0 → 0: si x fuera float el resultado sería 0.0.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 610:** `    (?) ¿Por qué no x / 1 → x? Porque '/' en este lenguaje siempre da float.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 611:** `    """`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 612:** `    consts = {q.dest: q.a for q in quads if q.op == 'CONST'}`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 614:** `    def is_int(name, value):`  
**Para qué sirve:** Define la función `is_int` y sus parámetros de entrada.  

**Línea 615:** `        v = consts.get(name)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 616:** `        return type(v) is int and v == value       # type() estricto: True no cuenta como 1`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 618:** `    out, notes = [], []`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 619:** `    for q in quads:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 620:** `        if q.op == 'BIN':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 621:** `            op, right = q.b`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 622:** `            new = None`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 623:** `            if op in ('+', '-') and is_int(right, 0):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 624:** `                new = Quad('MOV', q.a, None, q.dest, q.line); rule = f'x {op} 0 = x'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 625:** `            elif op == '+' and is_int(q.a, 0):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 626:** `                new = Quad('MOV', right, None, q.dest, q.line); rule = '0 + x = x'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 627:** `            elif op == '*' and is_int(right, 1):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 628:** `                new = Quad('MOV', q.a, None, q.dest, q.line); rule = 'x * 1 = x'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 629:** `            elif op == '*' and is_int(q.a, 1):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 630:** `                new = Quad('MOV', right, None, q.dest, q.line); rule = '1 * x = x'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 631:** `            elif op == '*' and is_int(right, 2) and not is_temp_const(q.a, consts):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 632:** `                new = Quad('BIN', q.a, ('+', q.a), q.dest, q.line); rule = 'x * 2 = x + x'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 633:** `            elif op == '*' and is_int(q.a, 2) and not is_temp_const(right, consts):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 634:** `                new = Quad('BIN', right, ('+', right), q.dest, q.line); rule = '2 * x = x + x'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 635:** `            if new:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 636:** `                notes.append(f'Línea {q.line}: simplificación algebraica ({rule}) en {q.dest}')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 637:** `                q = new`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 638:** `        out.append(q)`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 639:** `    return out, notes`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 642:** `def is_temp_const(name, consts):`  
**Para qué sirve:** Define la función `is_temp_const` y sus parámetros de entrada.  

**Línea 643:** `    # Si ambos lados son constantes, mejor dejar que el plegado calcule el valor final.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 644:** `    return name in consts`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 647:** `def eliminate_dead_temporaries(quads):`  
**Para qué sirve:** Define la función `eliminate_dead_temporaries` y sus parámetros de entrada.  

**Línea 648:** `    """DCE conservador: borra definiciones de temporales tN que nadie lee.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 650:** `    Recorre AL REVÉS (de abajo hacia arriba) manteniendo el conjunto \`live\` de`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 651:** `    nombres que se usarán más adelante: es un análisis de vida (liveness) hacia atrás.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 652:** `    No toca variables del usuario, PRINT, CALL ni operaciones de memoria (efectos laterales).`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 653:** `    """`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 654:** `    live, kept, notes = set(), [], []`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 655:** `    for q in reversed(quads):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 656:** `        if q.op in ('CONST', 'MOV', 'BIN') and is_temp(q.dest) and q.dest not in live:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 657:** `            notes.append(f'Línea {q.line}: temporal muerto {q.dest} eliminado')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 658:** `            continue`  
**Para qué sirve:** Salta a la siguiente iteración del ciclo.  

**Línea 659:** `        if q.dest is not None and q.op in ('CONST', 'MOV', 'BIN', 'ALLOC'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 660:** `            live.discard(q.dest)                  # antes de esta definición, el valor viejo no importa`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 661:** `        if q.op == 'BIN':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 662:** `            live.add(q.a); live.add(q.b[1])`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 663:** `        elif q.op in ('MOV', 'PRINT', 'FREE', 'RET') and isinstance(q.a, str):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 664:** `            live.add(q.a)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 665:** `        kept.append(q)`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 666:** `    return list(reversed(kept)), list(reversed(notes))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 669:** `def optimize(quads):`  
**Para qué sirve:** Define la función `optimize` y sus parámetros de entrada.  

**Línea 670:** `    """Pipeline de optimización. Devuelve (quads_optimizados, notas_explicativas)."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 671:** `    quads, notes = simplify_algebraic(quads)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 673:** `    # Propagación + plegado de constantes. \`known\` = qué nombres valen una constante`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 674:** `    # conocida EN ESTE PUNTO del programa. Se vacía al cruzar ENTER/CALL/LEAVE porque`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 675:** `    # una llamada es una "caja negra" para un análisis local.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 676:** `    known, out = {}, []`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 677:** `    for q in quads:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 678:** `        if q.op == 'ENTER':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 679:** `            known = {}`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 680:** `        if q.op == 'CONST':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 681:** `            known[q.dest] = q.a`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 682:** `        elif q.op == 'MOV':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 683:** `            if q.a in known:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 684:** `                value = known[q.a]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 685:** `                q = Quad('CONST', value, None, q.dest, q.line)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 686:** `                known[q.dest] = value`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 687:** `                notes.append(f'Línea {q.line}: propagación de constante a {q.dest}')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 688:** `            else:`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 689:** `                known.pop(q.dest, None)            # se reasignó con algo desconocido: deja de ser constante`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 690:** `        elif q.op == 'BIN':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 691:** `            op, right = q.b`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 692:** `            if q.a in known and right in known:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 693:** `                try:`  
**Para qué sirve:** Inicia un bloque que puede producir excepciones controladas.  

**Línea 694:** `                    v = calculate(op, known[q.a], known[right])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 695:** `                    q = Quad('CONST', v, None, q.dest, q.line)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 696:** `                    known[q.dest] = v`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 697:** `                    notes.append(f'Línea {q.line}: plegado constante en {q.dest}')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 698:** `                except ZeroDivisionError:`  
**Para qué sirve:** Captura un error y permite manejarlo sin terminar abruptamente.  

**Línea 699:** `                    # No se "pliega" un error: se deja la instrucción para que`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 700:** `                    # falle en ejecución exactamente como lo haría sin optimizar.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 701:** `                    known.pop(q.dest, None)`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 702:** `            else:`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 703:** `                known.pop(q.dest, None)`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 704:** `        elif q.op in ('CALL', 'LEAVE'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 705:** `            known = {}`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 706:** `        out.append(q)`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 708:** `    # DCE solo sin llamadas: dentro de una función se podría leer un global cuyo`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 709:** `    # valor se calculó en main, y este análisis lineal no "ve" a través del CALL.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 710:** `    if not any(q.op in ('CALL', 'RET') for q in out):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 711:** `        out, dead_notes = eliminate_dead_temporaries(out)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 712:** `        notes.extend(dead_notes)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 713:** `    return out, notes`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 716:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 717:** `#  MEMORIA EN EJECUCIÓN — [S8] Stack de marcos (LIFO) y Heap`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 718:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 720:** `class Memory:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 721:** `    """Modelo lógico, no byte a byte: la pila es una lista de marcos y el heap un`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 722:** `    dict dirección → tamaño. Lo comparten el intérprete TAC y la CPU virtual."""`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 724:** `    def __init__(self):`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 725:** `        self.stack = []`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 726:** `        self.heap = {}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 727:** `        self.next_addr = 0x1000          # bump allocator: nunca reutiliza direcciones liberadas`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 728:** `        self.events = []`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 730:** `    def push(self, name):`  
**Para qué sirve:** Define la función `push` y sus parámetros de entrada.  

**Línea 731:** `        self.stack.append({'function': name, 'locals': {}})`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 732:** `        self.events.append(f'PUSH frame {name}')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 734:** `    def pop(self):`  
**Para qué sirve:** Define la función `pop` y sus parámetros de entrada.  

**Línea 735:** `        if not self.stack:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 736:** `            raise RuntimeError('Stack underflow')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 737:** `        name = self.stack.pop()['function']   # al salir, los locales se destruyen solos (gestión automática)`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 738:** `        self.events.append(f'POP frame {name}')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 740:** `    def alloc(self, size):`  
**Para qué sirve:** Define la función `alloc` y sus parámetros de entrada.  

**Línea 741:** `        addr = self.next_addr`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 742:** `        self.next_addr += size`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 743:** `        self.heap[addr] = size`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 744:** `        self.events.append(f'HEAP ALLOC {size} bytes en {hex(addr)}')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 745:** `        return addr                      # el "ticket del estacionamiento" (S8)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 747:** `    def free(self, addr):`  
**Para qué sirve:** Define la función `free` y sus parámetros de entrada.  

**Línea 748:** `        # Como el allocator nunca reutiliza direcciones, un segundo free de la misma`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 749:** `        # dirección SIEMPRE se detecta (en malloc real podría pasar desapercibido).`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 750:** `        if addr not in self.heap:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 751:** `            raise RuntimeError(f'Doble free o puntero inválido: {hex(addr)}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 752:** `        del self.heap[addr]`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 753:** `        self.events.append(f'HEAP FREE {hex(addr)}')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 756:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 757:** `#  FASE 6 · GENERACIÓN DE CÓDIGO OBJETIVO — [S10] selección, registros y spill`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 758:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 760:** `OPCODES = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV',`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 761:** `           '==': 'EQ', '!=': 'NE', '<': 'LT', '>': 'GT', '<=': 'LE', '>=': 'GE',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 762:** `           '&&': 'AND', '&#124;&#124;': 'OR'}`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 765:** `class Backend:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 766:** `    """TAC → ensamblador de una ISA virtual de 3 operandos (estilo RISC: OP dest, src1, src2).`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 768:** `    Estado del asignador:`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 769:** `        owners    registro → nombre que lo ocupa       (R0 → 't3')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 770:** `        locations nombre   → registro donde está       ('t3' → R0)   (mapa inverso)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 771:** `        slots     nombre   → dirección RAM de su spill ('a' → 0x2000)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 773:** `    (?) ¿Qué algoritmo usan? Asignación LOCAL a demanda (S10 "Naive/Local"), no`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 774:** `        coloreado de grafos. La víctima del spill es la de MENOS usos futuros:`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 775:** `        heurística barata; la óptima teórica (Belady) sería "la que se usa más tarde".`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 776:** `    (?) ¿Por qué mínimo 3 registros? Una instrucción BIN necesita a la vez dos`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 777:** `        operandos y un destino; con 2 registros no hay donde poner el tercero.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 778:** `    """`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 780:** `    def __init__(self, registers=3):`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 781:** `        if registers < 3:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 782:** `            raise ValueError('Se requieren al menos 3 registros para esta ISA de tres operandos')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 783:** `        self.regs = [f'R{i}' for i in range(registers)]`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 784:** `        self.owners = {}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 785:** `        self.locations = {}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 786:** `        self.asm = []`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 787:** `        self.events = []`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 788:** `        self.spills = 0`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 789:** `        self.slots = {}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 790:** `        self.slot = 0`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 792:** `    def emit(self, s):`  
**Para qué sirve:** Define la función `emit` y sus parámetros de entrada.  

**Línea 793:** `        self.asm.append(s)`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 795:** `    def uses(self, q):`  
**Para qué sirve:** Define la función `uses` y sus parámetros de entrada.  

**Línea 796:** `        """Nombres que la cuádrupla LEE (no los que escribe)."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 797:** `        if q.op == 'BIN': return [q.a, q.b[1]]`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 798:** `        if q.op in ('MOV', 'PRINT', 'FREE', 'RET'): return [q.a]`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 799:** `        return []`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 801:** `    def future(self, quads, i):`  
**Para qué sirve:** Define la función `future` y sus parámetros de entrada.  

**Línea 802:** `        # Liveness APROXIMADO: cuenta lecturas en todo lo que queda de la cinta.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 803:** `        # Sin saltos, "aparece más abajo" ≈ "está vivo". Con bucles esto dejaría de valer.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 804:** `        return Counter(x for q in quads[i + 1:] for x in self.uses(q) if isinstance(x, str))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 806:** `    def slot_for(self, name):`  
**Para qué sirve:** Define la función `slot_for` y sus parámetros de entrada.  

**Línea 807:** `        if name not in self.slots:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 808:** `            self.slots[name] = 0x2000 + self.slot * 8      # slots de 8 bytes en la zona de spill`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 809:** `            self.slot += 1`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 810:** `        return self.slots[name]`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 812:** `    def reg(self, name, quads, i, protect=()):`  
**Para qué sirve:** Define la función `reg` y sus parámetros de entrada.  

**Línea 813:** `        """Devuelve el registro donde vive \`name\`, cargándolo o haciendo spill si hace falta.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 815:** `        protect = nombres que NO pueden ser víctimas porque la instrucción actual`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 816:** `        los está usando (expulsar el operando izquierdo para cargar el derecho`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 817:** `        dejaría la instrucción sin uno de sus operandos).`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 818:** `        """`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 819:** `        if name in self.locations:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 820:** `            return self.locations[name]`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 821:** `        free = next((r for r in self.regs if r not in self.owners), None)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 822:** `        if free is None:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 823:** `            # ── SPILL: no hay registros libres (S10, los 5 pasos) ──`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 824:** `            counts = self.future(quads, i)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 825:** `            candidates = [(counts.get(v, 0), r, v) for r, v in self.owners.items() if v not in protect]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 826:** `            if not candidates:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 827:** `                raise RuntimeError('No hay registro libre para los operandos; aumente el pool')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 828:** `            _, free, victim = min(candidates)              # 2. elegir víctima (menos usos futuros)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 829:** `            if counts.get(victim, 0):                       # solo se guarda si alguien la volverá a leer:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 830:** `                addr = self.slot_for(victim)                # un valor muerto se descarta sin STORE`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 831:** `                self.emit(f'STORE [{hex(addr)}], {free} ; SPILL {victim}')          # 3. STORE a RAM`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 832:** `                self.events.append(f'SPILL {victim}: {free} → STACK[{hex(addr)}]')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 833:** `                self.spills += 1`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 834:** `            self.locations.pop(victim, None)`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 835:** `            self.owners.pop(free)`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 836:** `        self.owners[free] = name                            # 4. el registro queda para la nueva variable`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 837:** `        self.locations[name] = free`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 838:** `        if name in self.slots:                              # 5. si vivía en RAM, LOAD de vuelta`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 839:** `            self.emit(f'LOAD {free}, [{hex(self.slots[name])}] ; RECARGA {name}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 840:** `            self.events.append(f'RELOAD {name}: STACK → {free}')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 841:** `        return free`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 843:** `    def release_dead(self, quads, i):`  
**Para qué sirve:** Define la función `release_dead` y sus parámetros de entrada.  

**Línea 844:** `        # Tras cada instrucción, los registros de valores sin usos futuros quedan`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 845:** `        # libres: así 3 registros alcanzan para expresiones largas (reutilización).`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 846:** `        future = self.future(quads, i)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 847:** `        for reg, name in list(self.owners.items()):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 848:** `            if not future.get(name, 0):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 849:** `                self.owners.pop(reg)`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 850:** `                self.locations.pop(name, None)`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 852:** `    def generate(self, quads):`  
**Para qué sirve:** Define la función `generate` y sus parámetros de entrada.  

**Línea 853:** `        for i, q in enumerate(quads):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 854:** `            if q.op in ('ENTER', 'LEAVE', 'CALL'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 855:** `                if q.op == 'CALL':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 856:** `                    # Convención "caller-saved": la función llamada puede usar`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 857:** `                    # cualquier registro, así que el llamador guarda en RAM lo que`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 858:** `                    # aún necesita ANTES del salto. Al volver se recarga vía slots.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 859:** `                    future = self.future(quads, i)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 860:** `                    for register, name in list(self.owners.items()):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 861:** `                        if future.get(name, 0):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 862:** `                            addr = self.slot_for(name)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 863:** `                            self.emit(f'STORE [{hex(addr)}], {register} ; CONSERVAR {name} ANTES DE CALL')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 864:** `                            self.events.append(f'CALL-SAVE {name}: {register} → STACK[{hex(addr)}]')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 865:** `                self.emit(f'{q.op} {q.a}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 866:** `                self.owners.clear()`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 867:** `                self.locations.clear()           # tras cruzar un límite de función, ningún registro es confiable`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 868:** `            elif q.op == 'CONST':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 869:** `                r = self.reg(q.dest, quads, i)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 870:** `                self.emit(f'LI {r}, {q.a!r} ; {q.dest}')          # LI = load immediate`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 871:** `            elif q.op == 'MOV':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 872:** `                source = self.reg(q.a, quads, i)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 873:** `                dest = self.reg(q.dest, quads, i, protect=(q.a,))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 874:** `                self.emit(f'MOV {dest}, {source} ; {q.dest}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 875:** `            elif q.op == 'BIN':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 876:** `                op, right = q.b`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 877:** `                leftreg = self.reg(q.a, quads, i)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 878:** `                rightreg = self.reg(right, quads, i, protect=(q.a,))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 879:** `                dest = self.reg(q.dest, quads, i, protect=(q.a, right))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 880:** `                # Selección de instrucciones: aquí es 1 a 1 (cada operador TAC tiene`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 881:** `                # su opcode). En x86 real, "t1 = a + b" podría ser MOV+ADD o un LEA.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 882:** `                self.emit(f'{OPCODES[op]} {dest}, {leftreg}, {rightreg} ; {q.dest}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 883:** `            elif q.op == 'PRINT':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 884:** `                self.emit(f'PRINT {self.reg(q.a, quads, i)}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 885:** `            elif q.op == 'ALLOC':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 886:** `                self.emit(f'ALLOC {self.reg(q.dest, quads, i)}, {q.a}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 887:** `            elif q.op == 'FREE':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 888:** `                self.emit(f'FREE {self.reg(q.a, quads, i)}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 889:** `            elif q.op == 'RET':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 890:** `                self.emit(f'RET {self.reg(q.a, quads, i)}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 891:** `            self.release_dead(quads, i)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 892:** `        return self.asm`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 895:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 896:** `#  INTÉRPRETE DE TAC — "oráculo" contra el cual se valida la CPU virtual`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 897:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 899:** `class Interpreter:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 900:** `    """Ejecuta las cuádruplas directamente (como el EmuladorVirtualIR de la S7).`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 902:** `    No sabe nada de registros ni de spill. Si su salida coincide con la de la CPU`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 903:** `    virtual, el back-end preservó la semántica (S10, reto 1 del back-end).`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 904:** `    """`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 906:** `    def __init__(self, quads):`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 907:** `        self.qs = quads`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 908:** `        self.memory = Memory()`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 909:** `        self.output = []`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 910:** `        self.globals = {}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 911:** `        self.locals = {}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 912:** `        self.calls = {}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 913:** `        self.return_value = None`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 915:** `    def val(self, k):`  
**Para qué sirve:** Define la función `val` y sus parámetros de entrada.  

**Línea 916:** `        if k in self.locals: return self.locals[k]      # mismo orden de búsqueda que Semantic.lookup:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 917:** `        if k in self.globals: return self.globals[k]    # primero el marco actual, luego el global`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 918:** `        raise RuntimeError(f'Variable temporal no inicializada: {k}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 920:** `    def execute(self):`  
**Para qué sirve:** Define la función `execute` y sus parámetros de entrada.  

**Línea 921:** `        entries = {q.a: i for i, q in enumerate(self.qs) if q.op == 'ENTER'}`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 922:** `        self.memory.push('main')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 923:** `        self.locals = {}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 924:** `        pc = entries['main'] + 1`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 925:** `        steps = 0`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 926:** `        while pc < len(self.qs):`  
**Para qué sirve:** Repite un bloque mientras la condición siga siendo verdadera.  

**Línea 927:** `            steps += 1`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 928:** `            if steps > 10000:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 929:** `                # Sin esto, una recursión f() { f(); } colgaría la GUI: es el "stack overflow" del simulador.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 930:** `                raise RuntimeError('Límite de ejecución alcanzado')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 931:** `            q = self.qs[pc]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 932:** `            op = q.op`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 933:** `            if op == 'CONST':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 934:** `                self.locals[q.dest] = q.a`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 935:** `            elif op == 'MOV':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 936:** `                v = self.val(q.a)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 937:** `                self.locals[q.dest] = v`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 938:** `                if not is_temp(q.dest):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 939:** `                    if len(self.memory.stack) == 1:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 940:** `                        self.globals[q.dest] = v`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 941:** `                    self.memory.stack[-1]['locals'][q.dest] = v`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 942:** `            elif op == 'BIN':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 943:** `                self.locals[q.dest] = calculate(q.b[0], self.val(q.a), self.val(q.b[1]))`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 944:** `            elif op == 'PRINT':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 945:** `                self.output.append(format_value(self.val(q.a)))`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 946:** `            elif op == 'ALLOC':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 947:** `                self.locals[q.dest] = self.memory.alloc(q.a)`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 948:** `            elif op == 'FREE':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 949:** `                self.memory.free(self.val(q.a))`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 950:** `            elif op == 'CALL':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 951:** `                if q.a not in entries:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 952:** `                    raise RuntimeError(f'Función no encontrada: {q.a}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 953:** `                # Dirección de retorno + entorno del llamador: lo que un stack frame real guarda.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 954:** `                self.calls[len(self.memory.stack)] = (pc + 1, self.locals)`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 955:** `                self.memory.push(q.a)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 956:** `                self.locals = {}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 957:** `                pc = entries[q.a] + 1`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 958:** `                continue`  
**Para qué sirve:** Salta a la siguiente iteración del ciclo.  

**Línea 959:** `            elif op in ('LEAVE', 'RET'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 960:** `                if op == 'RET':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 961:** `                    self.return_value = self.val(q.a)`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 962:** `                self.memory.pop()`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 963:** `                if not self.memory.stack:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 964:** `                    break                                  # se terminó main`  
**Para qué sirve:** Termina el ciclo actual.  

**Línea 965:** `                pc, self.locals = self.calls.pop(len(self.memory.stack))`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 966:** `                continue`  
**Para qué sirve:** Salta a la siguiente iteración del ciclo.  

**Línea 967:** `            pc += 1`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 968:** `        return self.output`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 971:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 972:** `#  ORQUESTADOR — conecta las fases y devuelve todo lo que la GUI muestra`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 973:** `# ════════════════════════════════════════════════════════════════════════════`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 975:** `def compile_source(source, registers=3, optimized=False, run=True):`  
**Para qué sirve:** Define la función `compile_source` y sus parámetros de entrada.  

**Línea 976:** `    """Ejecuta el pipeline completo. Nunca lanza excepciones hacia la GUI: cualquier`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 977:** `    error queda en result['error'] (S10, checklist: "sin detener abruptamente")."""`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 978:** `    result = {'source': source, 'error': None, 'error_phase': None}`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 979:** `    try:`  
**Para qué sirve:** Inicia un bloque que puede producir excepciones controladas.  

**Línea 980:** `        ts = lex(source)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 981:** `        result['tokens'] = [asdict(t) for t in ts]`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 982:** `        from automata import analyze_automata, GRAMMAR   # import tardío: automata no depende de compiler`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 983:** `        result['automata'] = analyze_automata(ts)`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 984:** `        result['grammar'] = GRAMMAR`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 986:** `        ast = Parser(ts).parse()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 987:** `        result['ast'] = ast.json()`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 989:** `        semantic = Semantic()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 990:** `        result['symbols'] = semantic.check(ast)`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 992:** `        raw = IRBuilder().build(ast)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 993:** `        result['tac'] = [q.show() for q in raw]`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 994:** `        # Se optimiza una COPIA para poder mostrar lado a lado TAC original vs optimizado.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 995:** `        opt, notes = optimize([Quad(**asdict(q)) for q in raw])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 996:** `        result['optimized_tac'] = [q.show() for q in opt]`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 997:** `        result['optimizations'] = notes`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 999:** `        chosen = opt if optimized else raw`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 1000:** `        result['quads'] = [asdict(q) for q in chosen]`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1001:** `        backend = Backend(registers)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 1002:** `        result['assembly'] = backend.generate(chosen)`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1003:** `        result['register_events'] = backend.events`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1004:** `        result['spill_count'] = backend.spills`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1005:** `        result['register_slots'] = {name: hex(addr) for name, addr in backend.slots.items()}`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1007:** `        if run:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 1008:** `            vm = Interpreter(chosen)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 1009:** `            result['output'] = vm.execute()`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1010:** `            result['memory_events'] = vm.memory.events`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1011:** `            result['globals'] = vm.globals`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1012:** `            result['heap_remaining'] = vm.memory.heap`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1014:** `            from virtual_cpu import VirtualCPU             # import tardío: virtual_cpu importa compiler`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 1015:** `            cpu = VirtualCPU(result['assembly'], registers)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 1016:** `            result['cpu_output'] = cpu.execute()`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1017:** `            result['cpu_trace'] = cpu.trace`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1018:** `            result['cpu_registers'] = cpu.registers`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1019:** `            result['cpu_ram'] = {hex(k): v for k, v in cpu.ram.items()}`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1020:** `            result['cpu_memory_events'] = cpu.memory.events`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1021:** `            result['cpu_heap_remaining'] = {hex(k): v for k, v in cpu.memory.heap.items()}`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1022:** `            # Validación cruzada: dos ejecuciones independientes (TAC vs ensamblador)`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 1023:** `            # deben imprimir lo mismo; si no, el bug está en el back-end.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 1024:** `            result['cpu_matches_tac'] = (result['cpu_output'] == result['output'])`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1025:** `            if not result['cpu_matches_tac']:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 1026:** `                raise RuntimeError(f'Diferencia entre TAC {result["output"]} y CPU {result["cpu_output"]}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 1027:** `        result['success'] = True`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1028:** `    except CompileError as e:`  
**Para qué sirve:** Captura un error y permite manejarlo sin terminar abruptamente.  

**Línea 1029:** `        result['success'] = False`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1030:** `        result['error'] = str(e)`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1031:** `        result['error_phase'] = e.phase`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1032:** `    except (RuntimeError, ZeroDivisionError, TypeError, ValueError) as e:`  
**Para qué sirve:** Captura un error y permite manejarlo sin terminar abruptamente.  

**Línea 1033:** `        # Lo que pasa DESPUÉS de compilar (doble free, división por cero con`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 1034:** `        # variables, límite de pasos) es un error de ejecución, no de compilación.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 1035:** `        result['success'] = False`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1036:** `        result['error'] = str(e)`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1037:** `        result['error_phase'] = 'Ejecución'`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 1038:** `    return result`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

## `automata.py`

**Línea 1:** `"""AFD didácticos (S2) y gramática del lenguaje (S3-S4).`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 3:** `IMPORTANTE para la sustentación: el lexer de producción (compiler.lex) usa la`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 4:** `regex maestra; estos AFD se ejecutan EN PARALELO sobre los lexemas ya reconocidos`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 5:** `para mostrar, estado por estado, qué máquina hay "debajo" de una regex.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 7:** `Ruta teórica completa (S2):  RegEx ─Thompson─► AFN ─subconjuntos─► AFD ─Hopcroft─► AFD mínimo`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 8:** `Aquí se escriben directamente los AFD mínimos de dos patrones; la construcción`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 9:** `automática (Thompson, subconjuntos, Hopcroft) no está implementada.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 10:** `"""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 11:** `from dataclasses import dataclass`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 14:** `@dataclass`  
**Para qué sirve:** Genera automáticamente métodos para una clase de datos.  

**Línea 15:** `class DFAResult:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 16:** `    accepted: bool`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 17:** `    state: str`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 18:** `    trace: list`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 21:** `def char_class(ch):`  
**Para qué sirve:** Define la función `char_class` y sus parámetros de entrada.  

**Línea 22:** `    """Alfabeto de entrada COMPRIMIDO: en vez de una columna por carácter (256+),`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 23:** `    la tabla tiene una columna por clase. Es la misma idea que usan los generadores`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 24:** `    de lexers (flex) para que la matriz quepa en memoria."""`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 25:** `    if ch.isascii() and (ch.isalpha() or ch == '_'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 26:** `        return 'letra'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 27:** `    if ch.isascii() and ch.isdigit():`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 28:** `        return 'digito'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 29:** `    if ch == '.':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 30:** `        return 'punto'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 31:** `    return 'otro'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 34:** `# Matrices de transición δ(estado, clase) → estado.  [S2 "Simulación de matriz de transición"]`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 35:** `# Una celda que NO existe equivale a ir al estado sumidero ERROR (rechazo).`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 36:** `IDENTIFIER_TABLE = {`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 37:** `    'q0': {'letra': 'q1'},                       # un ID no puede empezar con dígito: "2vida" es error léxico`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 38:** `    'q1': {'letra': 'q1', 'digito': 'q1'},`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 39:** `}`  
**Para qué sirve:** Cierra una estructura o agrupación abierta previamente.  

**Línea 40:** `IDENTIFIER_ACCEPT = {'q1'}`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 42:** `NUMBER_TABLE = {`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 43:** `    'q0':      {'digito': 'entero'},`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 44:** `    'entero':  {'digito': 'entero', 'punto': 'punto'},`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 45:** `    'punto':   {'digito': 'decimal'},            # "1." se queda en 'punto', que NO acepta`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 46:** `    'decimal': {'digito': 'decimal'},            # un segundo '.' no tiene celda → ERROR ("1.2.3")`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 47:** `}`  
**Para qué sirve:** Cierra una estructura o agrupación abierta previamente.  

**Línea 48:** `NUMBER_ACCEPT = {'entero', 'decimal'}`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 51:** `def run_dfa(table, accepting, word, start='q0'):`  
**Para qué sirve:** Define la función `run_dfa` y sus parámetros de entrada.  

**Línea 52:** `    """Simulador genérico: O(n) en la longitud del lexema y O(1) por paso`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 53:** `    (una búsqueda en la tabla). No hay retroceso: eso es lo que gana un AFD frente a un AFN."""`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 54:** `    state, trace = start, []`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 55:** `    for ch in word:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 56:** `        nxt = table.get(state, {}).get(char_class(ch), 'ERROR')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 57:** `        trace.append({'caracter': ch, 'desde': state, 'hasta': nxt})`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 58:** `        state = nxt`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 59:** `        if state == 'ERROR':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 60:** `            # El sumidero no tiene salida: el resto del lexema ya no puede ser aceptado.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 61:** `            break`  
**Para qué sirve:** Termina el ciclo actual.  

**Línea 62:** `    return DFAResult(state in accepting, state, trace)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 65:** `def identifier_dfa(word):`  
**Para qué sirve:** Define la función `identifier_dfa` y sus parámetros de entrada.  

**Línea 66:** `    return run_dfa(IDENTIFIER_TABLE, IDENTIFIER_ACCEPT, word)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 69:** `def number_dfa(word):`  
**Para qué sirve:** Define la función `number_dfa` y sus parámetros de entrada.  

**Línea 70:** `    return run_dfa(NUMBER_TABLE, NUMBER_ACCEPT, word)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 73:** `def analyze_automata(tokens):`  
**Para qué sirve:** Define la función `analyze_automata` y sus parámetros de entrada.  

**Línea 74:** `    """Recorre los tokens ID/NUMBER y documenta la traza de su AFD (pestaña Autómatas)."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 75:** `    output = []`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 76:** `    for t in tokens:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 77:** `        if t.kind in ('ID', 'NUMBER'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 78:** `            dfa = identifier_dfa(t.value) if t.kind == 'ID' else number_dfa(t.value)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 79:** `            output.append({'lexema': t.value, 'tipo': t.kind, 'aceptado': dfa.accepted,`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 80:** `                           'estado_final': dfa.state, 'transiciones': dfa.trace})`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 81:** `    return output`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 84:** `# Gramática en EBNF. Cada no terminal es una función del compiler.Parser.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 85:** `# Niveles de expresión de MENOR a MAYOR precedencia: más abajo = se agrupa primero.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 86:** `# (?) ¿Por qué esto es libre de contexto y no regular? Por '(' expr ')': los paréntesis`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 87:** `#     anidados necesitan "contar", y un autómata finito no tiene pila (S4).`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 88:** `GRAMMAR = '''program     -> statement* EOF`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 89:** `statement   -> TYPE ID '=' expr ';'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 90:** `             &#124; ID '=' expr ';' &#124; 'print' '(' expr ')' ';'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 91:** `             &#124; 'free' '(' ID ')' ';' &#124; ID '(' ')' ';'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 92:** `             &#124; 'fn' ID '(' ')' '{' statement* '}'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 93:** `             &#124; 'return' expr ';'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 94:** `expr        -> logic_or`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 95:** `logic_or    -> logic_and ('&#124;&#124;' logic_and)*`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 96:** `logic_and   -> comparison ('&&' comparison)*`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 97:** `comparison  -> addition (('=='&#124;'!='&#124;'<'&#124;'>'&#124;'<='&#124;'>=') addition)*`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 98:** `addition    -> multiply (('+'&#124;'-') multiply)*`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 99:** `multiply    -> unary (('*'&#124;'/') unary)*`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 100:** `unary       -> '-' unary &#124; '!' unary &#124; atom`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 101:** `atom        -> NUMBER &#124; STRING &#124; 'true' &#124; 'false' &#124; ID`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 102:** `             &#124; 'new' '(' NUMBER ')' &#124; '(' expr ')'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 103:** `TYPE        -> 'int' &#124; 'float' &#124; 'string' &#124; 'bool'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 104:** `'''`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

## `virtual_cpu.py`

**Línea 1:** `"""CPU virtual: ejecuta la ISA textual que emite compiler.Backend.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 3:** `Ciclo clásico fetch → decode → execute (como una CPU real, pero sobre texto):`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 4:** `    fetch   = leer self.instructions[self.pc]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 5:** `    decode  = separar opcode y operandos ("ADD R2, R0, R1" → 'ADD', ['R2','R0','R1'])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 6:** `    execute = actualizar registros / RAM / pila y mover el PC`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 8:** `Los registros son un banco LIMITADO (el mismo número que usó el Backend); la RAM`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 9:** `es un dict dirección → valor donde viven los spills (0x2000...). ENTER/LEAVE modelan`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 10:** `marcos de función, no son instrucciones x86.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 11:** `(?) ¿Es ensamblador real? No: es una ISA propia. Lo que se demuestra es que el`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 12:** `    código objetivo es EJECUTABLE y produce lo mismo que el TAC (semántica preservada).`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 13:** `"""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 14:** `import ast`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 15:** `import re`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 17:** `from compiler import Memory, calculate, format_value`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 19:** `ADDRESS = re.compile(r'\[(0x[0-9a-fA-F]+)\]')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 21:** `# opcode de 3 operandos → operador de calculate(). Es la inversa de compiler.OPCODES:`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 22:** `# si alguien agrega un operador al Backend y olvida este mapa, la CPU lo rechaza.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 23:** `ALU = {'ADD': '+', 'SUB': '-', 'MUL': '*', 'DIV': '/',`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 24:** `       'EQ': '==', 'NE': '!=', 'LT': '<', 'GT': '>', 'LE': '<=', 'GE': '>=',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 25:** `       'AND': '&&', 'OR': '&#124;&#124;'}`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 28:** `class VirtualCPU:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 29:** `    def __init__(self, assembly, register_count=3):`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 30:** `        self.instructions = list(assembly)`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 31:** `        # None = registro "sin inicializar": leerlo es un bug del Backend, no un 0 silencioso.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 32:** `        self.registers = {f'R{i}': None for i in range(register_count)}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 33:** `        self.ram = {}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 34:** `        self.memory = Memory()`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 35:** `        self.output = []`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 36:** `        self.trace = []`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 37:** `        self.pc = 0`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 38:** `        self.calls = []          # pila de direcciones de retorno (lo que en x86 empuja CALL)`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 39:** `        self.labels = {}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 40:** `        # Pre-pasada: resolver etiquetas ANTES de ejecutar (como lo hace un ensamblador`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 41:** `        # de dos pasadas), para poder saltar a funciones definidas más abajo.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 42:** `        for index, raw in enumerate(self.instructions):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 43:** `            instruction = raw.split(';', 1)[0].strip()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 44:** `            if instruction.startswith('ENTER '):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 45:** `                self.labels[instruction.split()[1]] = index`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 47:** `    def register(self, name):`  
**Para qué sirve:** Define la función `register` y sus parámetros de entrada.  

**Línea 48:** `        if name not in self.registers:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 49:** `            raise RuntimeError(f'Registro desconocido: {name}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 50:** `        value = self.registers[name]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 51:** `        if value is None:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 52:** `            raise RuntimeError(f'Lectura de registro no inicializado: {name} (PC={self.pc})')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 53:** `        return value`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 55:** `    def address(self, operand):`  
**Para qué sirve:** Define la función `address` y sus parámetros de entrada.  

**Línea 56:** `        match = ADDRESS.fullmatch(operand)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 57:** `        if not match:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 58:** `            raise RuntimeError(f'CPU: dirección inválida {operand}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 59:** `        return int(match.group(1), 16)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 61:** `    def snapshot(self, pc, instruction):`  
**Para qué sirve:** Define la función `snapshot` y sus parámetros de entrada.  

**Línea 62:** `        """Foto del estado DESPUÉS de ejecutar \`instruction\`: alimenta la pestaña Paso a paso."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 63:** `        self.trace.append({'pc': pc, 'instruction': instruction,`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 64:** `                           'registers': dict(self.registers),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 65:** `                           'ram': {hex(k): v for k, v in self.ram.items()},`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 66:** `                           'stack': [f['function'] for f in self.memory.stack],`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 67:** `                           'heap': {hex(k): v for k, v in self.memory.heap.items()}})`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 69:** `    def execute(self):`  
**Para qué sirve:** Define la función `execute` y sus parámetros de entrada.  

**Línea 70:** `        if 'main' not in self.labels:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 71:** `            raise RuntimeError('No existe punto de entrada main')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 72:** `        self.pc = self.labels['main']`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 73:** `        steps = 0`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 74:** `        while self.pc < len(self.instructions):`  
**Para qué sirve:** Repite un bloque mientras la condición siga siendo verdadera.  

**Línea 75:** `            steps += 1`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 76:** `            if steps > 10000:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 77:** `                raise RuntimeError('CPU: límite de 10000 instrucciones')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 78:** `            # ── fetch ──`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 79:** `            raw = self.instructions[self.pc]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 80:** `            instruction = raw.split(';', 1)[0].strip()      # lo que va tras ';' es comentario del Backend`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 81:** `            if not instruction:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 82:** `                self.pc += 1`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 83:** `                continue`  
**Para qué sirve:** Salta a la siguiente iteración del ciclo.  

**Línea 84:** `            # ── decode ──`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 85:** `            op, _, rest = instruction.partition(' ')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 86:** `            args = [arg.strip() for arg in rest.split(',')] if rest else []`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 87:** `            before = self.pc`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 88:** `            jump = None`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 89:** `            # ── execute ──`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 90:** `            if op == 'ENTER':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 91:** `                self.memory.push(args[0])`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 92:** `            elif op == 'LEAVE':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 93:** `                self.memory.pop()`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 94:** `                if not self.calls:                 # LEAVE de main: fin del programa`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 95:** `                    self.snapshot(before, instruction)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 96:** `                    break`  
**Para qué sirve:** Termina el ciclo actual.  

**Línea 97:** `                jump = self.calls.pop()`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 98:** `            elif op == 'CALL':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 99:** `                if args[0] not in self.labels:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 100:** `                    raise RuntimeError(f'CPU: función no encontrada: {args[0]}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 101:** `                self.calls.append(self.pc + 1)     # dirección de retorno = instrucción siguiente`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 102:** `                jump = self.labels[args[0]]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 103:** `            elif op == 'RET':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 104:** `                self.memory.pop()`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 105:** `                if not self.calls:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 106:** `                    raise RuntimeError('CPU: RET sin llamada')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 107:** `                jump = self.calls.pop()`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 108:** `            elif op == 'LI':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 109:** `                self.registers[args[0]] = ast.literal_eval(args[1])   # literal seguro: nunca eval()`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 110:** `            elif op == 'MOV':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 111:** `                self.registers[args[0]] = self.register(args[1])`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 112:** `            elif op == 'STORE':                    # registro → RAM   (mitad "salida" de un spill)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 113:** `                self.ram[self.address(args[0])] = self.register(args[1])`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 114:** `            elif op == 'LOAD':                     # RAM → registro   (mitad "regreso" de un spill)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 115:** `                addr = self.address(args[1])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 116:** `                if addr not in self.ram:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 117:** `                    raise RuntimeError(f'CPU: lectura de RAM no inicializada: {hex(addr)}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 118:** `                self.registers[args[0]] = self.ram[addr]`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 119:** `            elif op in ALU:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 120:** `                self.registers[args[0]] = calculate(ALU[op], self.register(args[1]), self.register(args[2]))`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 121:** `            elif op == 'PRINT':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 122:** `                self.output.append(format_value(self.register(args[0])))`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 123:** `            elif op == 'ALLOC':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 124:** `                self.registers[args[0]] = self.memory.alloc(int(args[1]))`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 125:** `            elif op == 'FREE':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 126:** `                self.memory.free(self.register(args[0]))`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 127:** `            else:`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 128:** `                raise RuntimeError(f'CPU: instrucción desconocida: {instruction}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 129:** `            self.snapshot(before, instruction)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 130:** `            self.pc = jump if jump is not None else self.pc + 1`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 131:** `        return self.output`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

## `native_backend.py`

**Línea 1:** `"""Backend nativo: traduce el AST validado a C11 y lo compila con GCC o Clang.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 3:** `El resultado es un ejecutable de máquina REAL, no una CPU simulada.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 4:** `La selección de registros físicos corresponde al compilador C instalado.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 6:** `(?) ¿Entonces CompilaLab "usa" GCC? Solo en esta ruta opcional. Es la técnica`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 7:** `    "source-to-source" (transpilar a C) que usaron los primeros compiladores de C++`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 8:** `    (Cfront) y que hoy usan Nim o Vala: C funciona como una IR portátil y GCC hace`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 9:** `    el back-end (selección de instrucciones, registros reales, spill real).`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 10:** `    Para ver ese back-end:  gcc -S -O0 programa.c  → programa.s (x86/ARM real).`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 11:** `Note que se parte del AST y NO del TAC: el TAC ya perdió los tipos que C necesita`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 12:** `para declarar variables (int64_t, double, const char *).`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 13:** `"""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 14:** `from __future__ import annotations`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 15:** `import os`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 16:** `from pathlib import Path`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 17:** `import shutil`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 18:** `import subprocess`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 19:** `import tempfile`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 20:** `from dataclasses import dataclass`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 23:** `class NativeError(Exception):`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 24:** `    """Error de traducción, compilación o ejecución nativa."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 27:** `def c_string(value):`  
**Para qué sirve:** Define la función `c_string` y sus parámetros de entrada.  

**Línea 28:** `    """Escapa una cadena para convertirla en un literal C válido."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 29:** `    import json`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 30:** `    return json.dumps(value, ensure_ascii=True)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 33:** `class CEmitter:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 34:** `    """Genera C11 desde el AST de CompilaLab, respetando sus tipos y ámbitos."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 35:** `    def __init__(self):`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 36:** `        self.types = [{}]`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 37:** `        self.indent = 0`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 38:** `        self.lines = []`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 40:** `    def write(self, statement):`  
**Para qué sirve:** Define la función `write` y sus parámetros de entrada.  

**Línea 41:** `        self.lines.append('    ' * self.indent + statement)`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 43:** `    def lookup(self, name):`  
**Para qué sirve:** Define la función `lookup` y sus parámetros de entrada.  

**Línea 44:** `        for scope in reversed(self.types):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 45:** `            if name in scope:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 46:** `                return scope[name]`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 47:** `        raise NativeError(f'Variable no declarada: {name}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 49:** `    def expression(self, node):`  
**Para qué sirve:** Define la función `expression` y sus parámetros de entrada.  

**Línea 50:** `        if node.kind == 'number':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 51:** `            return node.value`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 52:** `        if node.kind == 'string':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 53:** `            return c_string(node.value)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 54:** `        if node.kind == 'boolean':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 55:** `            return 'true' if node.value else 'false'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 56:** `        if node.kind == 'variable':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 57:** `            return node.value`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 58:** `        if node.kind == 'not':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 59:** `            return f'(!{self.expression(node.children[0])})'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 60:** `        if node.kind == 'binary':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 61:** `            left, right = node.children`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 62:** `            if node.value == '/':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 63:** `                # CompilaLab define división real incluso para dos enteros.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 64:** `                return f'((double)({self.expression(left)}) / (double)({self.expression(right)}))'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 65:** `            # En C, "a" == "b" compara DIRECCIONES de memoria, no el texto:`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 66:** `            # la igualdad de cadenas exige strcmp para conservar la semántica del lenguaje.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 67:** `            if self.infer(left) == 'string' and self.infer(right) == 'string' and node.value in ('==', '!='):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 68:** `                test = '== 0' if node.value == '==' else '!= 0'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 69:** `                return f'(strcmp({self.expression(left)}, {self.expression(right)}) {test})'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 70:** `            return f'({self.expression(left)} {node.value} {self.expression(right)})'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 71:** `        if node.kind == 'new':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 72:** `            raise NativeError('new/free requieren gestión segura de memoria; no se traducen todavía al backend nativo')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 73:** `        raise NativeError(f'Expresión nativa no soportada: {node.kind}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 75:** `    def infer(self, node):`  
**Para qué sirve:** Define la función `infer` y sus parámetros de entrada.  

**Línea 76:** `        if node.kind == 'number':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 77:** `            return 'float' if '.' in node.value else 'int'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 78:** `        if node.kind == 'string':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 79:** `            return 'string'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 80:** `        if node.kind == 'boolean':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 81:** `            return 'bool'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 82:** `        if node.kind == 'variable':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 83:** `            return self.lookup(node.value)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 84:** `        if node.kind == 'not':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 85:** `            return 'bool'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 86:** `        if node.kind == 'binary':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 87:** `            if node.value in ('==', '!=', '<', '>', '<=', '>=', '&&', '&#124;&#124;'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 88:** `                return 'bool'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 89:** `            left = self.infer(node.children[0]); right = self.infer(node.children[1])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 90:** `            return 'float' if 'float' in (left, right) or node.value == '/' else 'int'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 91:** `        raise NativeError('No se puede inferir tipo')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 93:** `    def statement(self, node):`  
**Para qué sirve:** Define la función `statement` y sus parámetros de entrada.  

**Línea 94:** `        if node.kind == 'declare':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 95:** `            name, typ = node.value['name'], node.value['type']`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 96:** `            self.types[-1][name] = typ`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 97:** `            # Mapeo de tipos fuente → tipos C. int64_t fija el ancho (64 bits) para`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 98:** `            # que el resultado no dependa de la plataforma, como sí pasaría con "int".`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 99:** `            ctype = {'int': 'int64_t', 'float': 'double', 'bool': 'bool', 'string': 'const char *'}[typ]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 100:** `            self.write(f'{ctype} {name} = {self.expression(node.children[0])};')`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 101:** `        elif node.kind == 'assign':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 102:** `            self.write(f'{node.value} = {self.expression(node.children[0])};')`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 103:** `        elif node.kind == 'print':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 104:** `            expr = node.children[0]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 105:** `            typ = self.infer(expr)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 106:** `            fmt = {'int': '%" PRId64 "', 'float': '%.15g', 'bool': '%s', 'string': '%s'}[typ]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 107:** `            value = self.expression(expr)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 108:** `            if typ == 'bool':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 109:** `                value = f'(({value}) ? "true" : "false")'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 110:** `            self.write(f'printf("{fmt}\\n", {value});')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 111:** `        elif node.kind == 'call':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 112:** `            self.write(f'{node.value}();')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 113:** `        elif node.kind == 'return':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 114:** `            raise NativeError('Las funciones con return no tienen valor de retorno en la sintaxis actual; se requiere ampliar el lenguaje')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 115:** `        elif node.kind == 'free':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 116:** `            raise NativeError('free requiere gestión segura de memoria; no se traduce todavía al backend nativo')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 117:** `        else:`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 118:** `            raise NativeError(f'Sentencia nativa no soportada: {node.kind}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 120:** `    def generate(self, ast):`  
**Para qué sirve:** Define la función `generate` y sus parámetros de entrada.  

**Línea 121:** `        self.lines = [`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 122:** `            '/* CompilaLab: C11 generado desde AST validado. */',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 123:** `            '#include <stdio.h>',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 124:** `            '#include <stdint.h>',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 125:** `            '#include <inttypes.h>',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 126:** `            '#include <stdbool.h>',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 127:** `            '#include <string.h>',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 128:** `            '',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 129:** `        ]`  
**Para qué sirve:** Cierra una estructura o agrupación abierta previamente.  

**Línea 130:** `        functions = [n for n in ast.children if n.kind == 'function']`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 131:** `        # Las funciones usan el mismo espacio de nombres global que el programa.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 132:** `        for fn in functions:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 133:** `            self.write(f'static void {fn.value}(void);')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 134:** `        if functions:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 135:** `            self.write('')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 136:** `        for fn in functions:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 137:** `            # Una función nativa no puede leer variables locales de main.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 138:** `            # Se rechaza expresamente en lugar de producir C incorrecto.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 139:** `            global_names = {n.value['name'] for n in ast.children if n.kind == 'declare'}`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 140:** `            def walk(n):`  
**Para qué sirve:** Define la función `walk` y sus parámetros de entrada.  

**Línea 141:** `                if n.kind == 'variable' and n.value in global_names:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 142:** `                    raise NativeError(f'La función {fn.value} accede a {n.value} de main: alcance nativo aún no soportado')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 143:** `                for child in n.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 144:** `                    walk(child)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 145:** `            for stmt in fn.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 146:** `                for child in stmt.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 147:** `                    walk(child)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 148:** `            self.write(f'static void {fn.value}(void) {{')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 149:** `            self.indent = 1`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 150:** `            self.types.append({})`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 151:** `            for stmt in fn.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 152:** `                self.statement(stmt)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 153:** `            self.types.pop()`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 154:** `            self.indent = 0`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 155:** `            self.write('}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 156:** `        self.write('int main(void) {')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 157:** `        self.indent = 1`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 158:** `        for stmt in ast.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 159:** `            if stmt.kind != 'function':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 160:** `                self.statement(stmt)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 161:** `        self.write('return 0;')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 162:** `        self.indent = 0`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 163:** `        self.write('}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 164:** `        return '\n'.join(self.lines) + '\n'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 167:** `def find_compiler():`  
**Para qué sirve:** Define la función `find_compiler` y sus parámetros de entrada.  

**Línea 168:** `    """Busca un compilador real instalado y disponible en PATH."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 169:** `    for name in ('gcc', 'clang'):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 170:** `        found = shutil.which(name)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 171:** `        if found:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 172:** `            return found`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 173:** `    return None`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 176:** `def build_native(source, destination=None, run=True, timeout=8):`  
**Para qué sirve:** Define la función `build_native` y sus parámetros de entrada.  

**Línea 177:** `    """Compila código CompilaLab a ejecutable nativo; devuelve C, binario y salida.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 179:** `    El código fuente se valida primero con el frontend del proyecto. Nunca`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 180:** `    se pasa el texto original del usuario como código C sin analizar.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 181:** `    """`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 182:** `    from compiler import lex, Parser, Semantic`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 183:** `    compiler = find_compiler()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 184:** `    if not compiler:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 185:** `        raise NativeError('No se encontró GCC ni Clang en PATH. Instala MinGW-w64 o LLVM para compilar de forma nativa.')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 186:** `    tree = Parser(lex(source)).parse()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 187:** `    Semantic().check(tree)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 188:** `    generated = CEmitter().generate(tree)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 189:** `    if destination is None:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 190:** `        folder = Path(tempfile.mkdtemp(prefix='compilalab_native_'))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 191:** `        destination = folder / ('programa.exe' if os.name == 'nt' else 'programa')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 192:** `    else:`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 193:** `        destination = Path(destination).resolve()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 194:** `        destination.parent.mkdir(parents=True, exist_ok=True)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 195:** `    c_path = destination.with_suffix('.c')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 196:** `    c_path.write_text(generated, encoding='utf-8')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 197:** `    cmd = [compiler, '-std=c11', '-O0', '-Wall', '-Wextra', str(c_path), '-o', str(destination)]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 198:** `    try:`  
**Para qué sirve:** Inicia un bloque que puede producir excepciones controladas.  

**Línea 199:** `        build = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 200:** `    except subprocess.TimeoutExpired as error:`  
**Para qué sirve:** Captura un error y permite manejarlo sin terminar abruptamente.  

**Línea 201:** `        raise NativeError('El compilador nativo superó el tiempo límite') from error`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 202:** `    if build.returncode:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 203:** `        raise NativeError('Error del compilador C:\n' + build.stderr[-4000:])`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 204:** `    output = None`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 205:** `    if run:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 206:** `        try:`  
**Para qué sirve:** Inicia un bloque que puede producir excepciones controladas.  

**Línea 207:** `            executed = subprocess.run([str(destination)], capture_output=True, text=True, timeout=timeout, check=False)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 208:** `        except subprocess.TimeoutExpired as error:`  
**Para qué sirve:** Captura un error y permite manejarlo sin terminar abruptamente.  

**Línea 209:** `            raise NativeError('El ejecutable nativo superó el tiempo límite') from error`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 210:** `        if executed.returncode:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 211:** `            raise NativeError(f'El programa nativo terminó con código {executed.returncode}: {executed.stderr[-2000:]}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 212:** `        output = executed.stdout`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 213:** `    return {'c_source': generated, 'c_path': str(c_path), 'executable': str(destination),`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 214:** `            'compiler': compiler, 'build_warnings': build.stderr, 'output': output}`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

## `gui.py`

**Línea 1:** `"""Interfaz gráfica (Tkinter, sin dependencias externas).`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 3:** `(?) ¿Esta GUI es el "front-end" del compilador? NO. Front-end del compilador =`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 4:** `    léxico + sintaxis + semántica (compiler.py). Esto es la interfaz de USUARIO:`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 5:** `    solo llama a compile_source() y pinta el diccionario que devuelve. Se podría`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 6:** `    reemplazar por main.py (consola) sin tocar una línea del compilador.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 7:** `"""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 8:** `import json`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 9:** `import tkinter as tk`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 10:** `from tkinter import ttk, filedialog`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 11:** `from pathlib import Path`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 12:** `from compiler import compile_source`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 13:** `from coverage import COVERAGE`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 14:** `from native_backend import build_native, NativeError, find_compiler`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 16:** `BASE=Path(__file__).resolve().parent`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 17:** `root=tk.Tk(); root.title('CompilaLab v11 &#124; Laboratorio integral de compiladores'); root.geometry('1420x850')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 18:** `root.configure(bg='#101b2c')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 19:** `style=ttk.Style(); style.theme_use('clam')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 20:** `style.configure('TNotebook',background='#101b2c'); style.configure('TNotebook.Tab',padding=(15,9))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 21:** `header=tk.Frame(root,bg='#101b2c'); header.pack(fill='x',padx=20,pady=(14,8))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 22:** `tk.Label(header,text='CompilaLab',font=('Segoe UI',24,'bold'),fg='#e9f4ff',bg='#101b2c').pack(side='left')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 23:** `tk.Label(header,text='  Lexer → AST → Semántica → TAC → CPU / RAM',font=('Segoe UI',11),fg='#92a6bf',bg='#101b2c').pack(side='left',padx=14)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 24:** `bar=tk.Frame(root,bg='#101b2c'); bar.pack(fill='x',padx=20,pady=7)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 25:** `reg=tk.IntVar(value=3); optimize=tk.BooleanVar(value=False)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 26:** `tk.Label(bar,text='Registros:',bg='#101b2c',fg='white').pack(side='left')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 27:** `ttk.Spinbox(bar,from_=3,to=16,textvariable=reg,width=4).pack(side='left',padx=6)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 28:** `ttk.Checkbutton(bar,text='Activar optimización',variable=optimize).pack(side='left',padx=15)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 29:** `status=tk.StringVar(value='Preparado para compilar')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 30:** `main=tk.PanedWindow(root,orient='horizontal',sashwidth=7,bg='#101b2c'); main.pack(fill='both',expand=True,padx=20,pady=8)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 31:** `left=tk.Frame(main,bg='#17263a'); right=tk.Frame(main,bg='#17263a'); main.add(left,minsize=350,width=450); main.add(right,minsize=500)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 32:** `tk.Label(left,text='CÓDIGO FUENTE',font=('Segoe UI',11,'bold'),bg='#17263a',fg='white').pack(anchor='w',padx=12,pady=10)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 33:** `editor=tk.Text(left,font=('Consolas',12),bg='#0e1828',fg='#dceeff',insertbackground='white',undo=True,wrap='none',padx=12,pady=12)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 34:** `editor.pack(fill='both',expand=True,padx=12,pady=(0,12)); editor.insert('1.0',(BASE/'examples'/'correcto.clab').read_text(encoding='utf-8'))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 35:** `notebook=ttk.Notebook(right); notebook.pack(fill='both',expand=True,padx=12,pady=12)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 36:** `views={}`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 37:** `for name in ['Tokens','Autómatas','Gramática','AST','Símbolos','TAC','Optimización','Ensamblador','Spill','Memoria','CPU virtual','Paso a paso','Cobertura','Salida','C nativo','Salida nativa']:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 38:** `    frame=tk.Frame(notebook,bg='#0e1828'); notebook.add(frame,text=name)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 39:** `    widget=tk.Text(frame,font=('Consolas',11),bg='#0e1828',fg='#dceeff',insertbackground='white',wrap='none',padx=14,pady=14)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 40:** `    widget.pack(fill='both',expand=True); views[name]=widget`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 42:** `last_result={}`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 43:** `step_index=tk.IntVar(value=0)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 45:** `def show_step():`  
**Para qué sirve:** Define la función `show_step` y sus parámetros de entrada.  

**Línea 46:** `    trace=last_result.get('cpu_trace',[])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 47:** `    if not trace:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 48:** `        message='Sin traza. Compila un programa válido.'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 49:** `    else:`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 50:** `        index=max(0,min(step_index.get(),len(trace)-1)); step_index.set(index)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 51:** `        message=json.dumps({'paso':index+1,'total':len(trace),**trace[index]},ensure_ascii=False,indent=2)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 52:** `    w=views['Paso a paso']; w.delete('1.0','end'); w.insert('1.0',message)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 54:** `def advance_step(delta):`  
**Para qué sirve:** Define la función `advance_step` y sus parámetros de entrada.  

**Línea 55:** `    step_index.set(step_index.get()+delta); show_step(); notebook.select(list(views).index('Paso a paso'))`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 57:** `def compile_action():`  
**Para qué sirve:** Define la función `compile_action` y sus parámetros de entrada.  

**Línea 58:** `    # Toda la compilación ocurre aquí; el resto de la función solo reparte el resultado en pestañas.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 59:** `    r=compile_source(editor.get('1.0','end-1c'),reg.get(),optimize.get())`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 60:** `    last_result.clear(); last_result.update(r); step_index.set(0)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 61:** `    data={'Tokens':r.get('tokens',[]),'Autómatas':r.get('automata',[]),'Gramática':r.get('grammar',''),'AST':r.get('ast',{}),'Símbolos':r.get('symbols',[]),'TAC':r.get('tac',[]),'Optimización':{'notas':r.get('optimizations',[]),'tac':r.get('optimized_tac',[])},'Ensamblador':r.get('assembly',[]),'Spill':{'cantidad':r.get('spill_count',0),'eventos':r.get('register_events',[]),'slots':r.get('register_slots',{})},'Memoria':{'eventos':r.get('memory_events',[]),'variables':r.get('globals',{}),'heap_pendiente':r.get('heap_remaining',{})},'CPU virtual':{'salida_cpu':r.get('cpu_output',[]),'coincide_con_tac':r.get('cpu_matches_tac'),'registros_finales':r.get('cpu_registers',{}),'ram_spill':r.get('cpu_ram',{}),'heap_final':r.get('cpu_heap_remaining',{}),'eventos_memoria':r.get('cpu_memory_events',[]),'traza':r.get('cpu_trace',[])},'Paso a paso':{},'Cobertura':[{'semana':week,'concepto':concept,'ubicacion':location,'estado':status} for week,concept,location,status in COVERAGE],'Salida':r.get('output',[])}`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 62:** `    for key,value in data.items():`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 63:** `        w=views[key]; w.delete('1.0','end'); w.insert('1.0','\n'.join(map(str,value)) if isinstance(value,list) and key not in ('Tokens','Símbolos') else json.dumps(value,ensure_ascii=False,indent=2))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 64:** `    show_step()`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 65:** `    status.set(('✓ Compilación exitosa · Spill: '+str(r.get('spill_count',0))) if r['success'] else '✗ ['+str(r.get('error_phase'))+'] '+r['error'])`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 66:** `    notebook.select(list(views).index('Salida') if r['success'] else 0)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 68:** `def native_action():`  
**Para qué sirve:** Define la función `native_action` y sus parámetros de entrada.  

**Línea 69:** `    # Traduce el programa al AST, genera C11, invoca GCC/Clang y ejecuta el binario real.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 70:** `    try:`  
**Para qué sirve:** Inicia un bloque que puede producir excepciones controladas.  

**Línea 71:** `        result = build_native(editor.get('1.0', 'end-1c'))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 72:** `        for tab, value in [('C nativo', result['c_source']), ('Salida nativa', result['output'])]:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 73:** `            views[tab].delete('1.0', 'end')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 74:** `            views[tab].insert('1.0', value)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 75:** `        status.set('✓ Compilación NATIVA exitosa: ' + result['executable'])`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 76:** `        notebook.select(list(views).index('Salida nativa'))`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 77:** `    except Exception as error:`  
**Para qué sirve:** Captura un error y permite manejarlo sin terminar abruptamente.  

**Línea 78:** `        # La interfaz informa el error y permanece abierta.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 79:** `        views['Salida nativa'].delete('1.0', 'end')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 80:** `        views['Salida nativa'].insert('1.0', str(error))`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 81:** `        status.set('✗ Compilación nativa fallida: ' + str(error)[:110])`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 82:** `        notebook.select(list(views).index('Salida nativa'))`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 84:** `def open_action():`  
**Para qué sirve:** Define la función `open_action` y sus parámetros de entrada.  

**Línea 85:** `    file=filedialog.askopenfilename(filetypes=[('CompilaLab','*.clab'),('Todos','*.*')])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 86:** `    if file: editor.delete('1.0','end'); editor.insert('1.0',Path(file).read_text(encoding='utf-8'))`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 88:** `def example(name):`  
**Para qué sirve:** Define la función `example` y sus parámetros de entrada.  

**Línea 89:** `    editor.delete('1.0','end'); editor.insert('1.0',(BASE/'examples'/name).read_text(encoding='utf-8')); compile_action()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 91:** `ttk.Button(bar,text='▶ Compilar y ejecutar',command=compile_action).pack(side='left',padx=8)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 92:** `ttk.Button(bar,text='▶ Ejecutable REAL (GCC/Clang)',command=native_action).pack(side='left',padx=5)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 93:** `ttk.Button(bar,text='Abrir archivo',command=open_action).pack(side='left',padx=8)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 94:** `for label,name in [('Correcto','correcto.clab'),('Spill','spill.clab'),('Tipos','tipos_error.clab'),('Léxico','errores_lexicos.clab'),('Stack / Heap','memoria.clab'),('Optimiz.','optimizacion.clab'),('Algebraica','algebraica.clab'),('Lógica','logica.clab')]:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 95:** `    ttk.Button(bar,text=label,command=lambda n=name:example(n)).pack(side='left',padx=3)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 96:** `ttk.Button(bar,text='◀ CPU',command=lambda:advance_step(-1)).pack(side='left',padx=3)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 97:** `ttk.Button(bar,text='CPU ▶',command=lambda:advance_step(1)).pack(side='left',padx=3)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 98:** `tk.Label(root,textvariable=status,anchor='w',font=('Segoe UI',11),bg='#101b2c',fg='#86d8c5').pack(fill='x',padx=20,pady=(0,12))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 99:** `compile_action(); root.mainloop()`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

## `coverage.py`

**Línea 1:** `"""Matriz teoría ↔ código: trazabilidad pedagógica, no certificación industrial.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 3:** `Estados:  Implementado = el algoritmo se ejecuta y tiene pruebas.`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 4:** `          Simulación   = modelo educativo (no hardware ni SO real).`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 5:** `          Parcial      = solo un subconjunto del concepto.`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 6:** `          Solo teoría  = se explica, no se ejecuta.`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 7:** `"""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 8:** `COVERAGE = [`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 9:** ` ('1','Arquitectura por fases (front/middle/back-end)','compiler.compile_source','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 10:** ` ('1','Clasificación de errores por fase','compiler.CompileError / error_phase','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 11:** ` ('2','Tokens, lexemas, patrones (regex con named groups)','compiler.PATTERN / lex','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 12:** ` ('2','Recuperación de errores léxicos (modo pánico)','compiler.lex','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 13:** ` ('2','Comentarios //, /* */ y cadenas (reto S2)','compiler.PATTERN','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 14:** ` ('2','AFD por matriz de transición','automata.run_dfa / *_TABLE','Implementado (didáctico)'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 15:** ` ('2','Thompson, subconjuntos, Hopcroft','docs/TEORIA_Y_LIMITACIONES.md','Solo teoría'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 16:** ` ('3','Gramática libre de contexto (EBNF)','automata.GRAMMAR','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 17:** ` ('3-4','Descenso recursivo Top-Down y AST','compiler.Parser / Node','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 18:** ` ('4','Precedencia y asociatividad sin recursión izquierda','compiler.Parser.binary_level','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 19:** ` ('4','Bottom-Up shift-reduce, LR/LALR','docs/TEORIA_Y_LIMITACIONES.md','Solo teoría'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 20:** ` ('5','Tabla de símbolos, pila de ámbitos, lookup','compiler.Semantic','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 21:** ` ('5','Shadowing local/global y redeclaración','compiler.Semantic.block','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 22:** ` ('5','Ámbitos de bloque (if/while)','—','Parcial (el lenguaje no tiene bloques)'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 23:** ` ('6','Inferencia, equivalencia y coerción int→float','compiler.Semantic.expr / compatible','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 24:** ` ('6','División por cero con divisor literal','compiler.Semantic.expr','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 25:** ` ('7','TAC, cuádruplas y temporales','compiler.IRBuilder / Quad','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 26:** ` ('7','Saltos condicionales (GOTO) en la IR','—','Solo teoría'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 27:** ` ('8','Stack LIFO, Stack Frames y Heap','compiler.Memory','Simulación'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 28:** ` ('9','Simplificación algebraica y reducción de fuerza','compiler.simplify_algebraic','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 29:** ` ('9','Propagación y plegado de constantes','compiler.optimize','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 30:** ` ('9','Eliminación de temporales muertos','compiler.eliminate_dead_temporaries','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 31:** ` ('9','Optimización global sobre CFG','docs/TEORIA_Y_LIMITACIONES.md','Solo teoría'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 32:** ` ('10','Selección de instrucciones, ensamblador','compiler.Backend','Implementado (ISA virtual)'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 33:** ` ('10','Asignación local de registros, liveness aproximado y Spill','compiler.Backend.reg','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 34:** ` ('10','Coloreado de grafos (Chaitin-Briggs)','docs/TEORIA_Y_LIMITACIONES.md','Solo teoría'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 35:** ` ('10','CPU virtual fetch-decode-execute y RAM de Spill','virtual_cpu.VirtualCPU','Simulación'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 36:** ` ('10','Ejecutable nativo vía C11 + GCC/Clang','native_backend.build_native','Implementado (parcial)'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 37:** ` ('10','Pruebas del pipeline y validación TAC vs CPU','tests/','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 38:** `]`  
**Para qué sirve:** Cierra una estructura o agrupación abierta previamente.  

## `main.py`

**Línea 1:** `"""Interfaz de consola: el mismo compile_source() que usa la GUI, impreso fase por fase.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 3:** `Ejemplo:  python main.py examples/spill.clab --registers 3`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 4:** `          python main.py examples/algebraica.clab --optimize`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 5:** `"""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 6:** `import argparse`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 7:** `import json`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 8:** `from pathlib import Path`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 9:** `from compiler import compile_source`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 11:** `BASE=Path(__file__).resolve().parent`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 13:** `def main():`  
**Para qué sirve:** Define la función `main` y sus parámetros de entrada.  

**Línea 14:** `    p=argparse.ArgumentParser(description='CompilaLab — compilador educativo')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 15:** `    p.add_argument('file',nargs='?',default=str(BASE/'examples'/'correcto.clab'))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 16:** `    p.add_argument('--registers',type=int,default=3)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 17:** `    p.add_argument('--optimize',action='store_true')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 18:** `    p.add_argument('--json',action='store_true')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 19:** `    a=p.parse_args()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 20:** `    if a.registers<3: p.error('Se requieren al menos 3 registros para esta ISA virtual')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 21:** `    source=Path(a.file).read_text(encoding='utf-8')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 22:** `    r=compile_source(source,a.registers,a.optimize)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 23:** `    if a.json: print(json.dumps(r,indent=2,ensure_ascii=False)); return`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 24:** `    print('=== CÓDIGO FUENTE ===\n'+source)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 25:** `    for key,title in [('tokens','TOKENS'),('ast','AST'),('symbols','TABLA DE SÍMBOLOS'),('tac','TAC'),('optimized_tac','TAC OPTIMIZADO'),('optimizations','OPTIMIZACIONES'),('assembly','ENSAMBLADOR VIRTUAL'),('register_events','REGISTROS Y SPILL'),('memory_events','MEMORIA STACK/HEAP'),('output','SALIDA')]:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 26:** `        if key in r: print(f'\n=== {title} ===\n'+(json.dumps(r[key],indent=2,ensure_ascii=False) if key in ('tokens','ast','symbols') else '\n'.join(map(str,r[key]))))`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 27:** `    print(f'\nSPILLS: {r.get("spill_count",0)}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 28:** `    print('OK' if r['success'] else f"ERROR [{r.get('error_phase')}]: {r['error']}")`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 30:** `if __name__=='__main__': main()`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

## `generar_guia_comentada.py`

**Línea 1:** `"""Genera un manual explicando cada línea no vacía del código del proyecto.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 3:** `Se escribe en Markdown para no insertar comentarios dentro de cadenas multilínea,`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 4:** `lo que podría romper el programa. Se mantiene el número de línea original.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 5:** `"""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 6:** `from pathlib import Path`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 7:** `import re`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 9:** `ROOT = Path(__file__).resolve().parent`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 10:** `OUTPUT = ROOT / 'docs' / 'CODIGO_LINEA_POR_LINEA.md'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 11:** `FILES = ['compiler.py', 'automata.py', 'virtual_cpu.py', 'native_backend.py',`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 12:** `         'gui.py', 'coverage.py', 'main.py', 'generar_guia_comentada.py']`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 15:** `def explain(line):`  
**Para qué sirve:** Define la función `explain` y sus parámetros de entrada.  

**Línea 16:** `    s = line.strip()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 17:** `    if s.startswith('#'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 18:** `        return 'Comentario original del desarrollador que explica el contexto.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 19:** `    if s.startswith('"""') or s.startswith("'''"):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 20:** `        return 'Inicio, continuación o cierre de documentación interna (docstring).'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 21:** `    if s.startswith('from ') or s.startswith('import '):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 22:** `        return 'Importa clases, funciones o módulos que necesita este archivo.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 23:** `    if s.startswith('@dataclass'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 24:** `        return 'Genera automáticamente métodos para una clase de datos.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 25:** `    if s.startswith('@'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 26:** `        return 'Decorador que modifica o configura la definición siguiente.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 27:** `    if s.startswith('class '):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 28:** `        return 'Declara una clase y define la responsabilidad de sus objetos.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 29:** `    if s.startswith('def '):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 30:** `        name = s.split('def ', 1)[1].split('(', 1)[0]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 31:** `        return f'Define la función \`{name}\` y sus parámetros de entrada.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 32:** `    if s.startswith('if ') or s.startswith('elif '):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 33:** `        return 'Evalúa una condición para decidir qué rama del algoritmo ejecutar.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 34:** `    if s.startswith('else:'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 35:** `        return 'Ejecuta la alternativa cuando no se cumple la condición anterior.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 36:** `    if s.startswith('for '):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 37:** `        return 'Itera sobre una secuencia o colección de elementos.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 38:** `    if s.startswith('while '):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 39:** `        return 'Repite un bloque mientras la condición siga siendo verdadera.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 40:** `    if s.startswith('try:'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 41:** `        return 'Inicia un bloque que puede producir excepciones controladas.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 42:** `    if s.startswith('except '):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 43:** `        return 'Captura un error y permite manejarlo sin terminar abruptamente.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 44:** `    if s.startswith('raise '):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 45:** `        return 'Lanza una excepción para indicar una condición inválida.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 46:** `    if s.startswith('return '):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 47:** `        return 'Devuelve el resultado de la función al código que la llamó.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 48:** `    if s.startswith('continue'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 49:** `        return 'Salta a la siguiente iteración del ciclo.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 50:** `    if s.startswith('break'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 51:** `        return 'Termina el ciclo actual.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 52:** `    if s.startswith('with '):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 53:** `        return 'Abre un contexto que gestiona automáticamente sus recursos.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 54:** `    if s.startswith('assert '):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 55:** `        return 'Verifica una condición que debe cumplirse.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 56:** `    if s.startswith('self.') and '=' in s:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 57:** `        return 'Actualiza el estado interno del objeto mediante un atributo.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 58:** `    if s.startswith('result['):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 59:** `        return 'Guarda información de una fase en el resultado de compilación.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 60:** `    if 'emit(' in s:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 61:** `        return 'Emite una instrucción o un registro para una fase posterior.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 62:** `    if 'append(' in s:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 63:** `        return 'Añade un elemento a una lista de trabajo o resultados.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 64:** `    if 'pop(' in s:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 65:** `        return 'Retira un elemento; en una pila sigue el principio LIFO.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 66:** `    if '=' in s and '==' not in s:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 67:** `        return 'Asigna o actualiza un valor que utilizará el algoritmo.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 68:** `    if s in ('}', ']', ')'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 69:** `        return 'Cierra una estructura o agrupación abierta previamente.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 70:** `    return 'Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 73:** `def generate():`  
**Para qué sirve:** Define la función `generate` y sus parámetros de entrada.  

**Línea 74:** `    sections = ['# CompilaLab — Guía de lectura línea por línea',`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 75:** `                '', 'Cada entrada conserva el número real de línea del archivo.',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 76:** `                'Las explicaciones son ayudas de lectura; las decisiones del algoritmo se estudian también con los tests.', '']`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 77:** `    for filename in FILES:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 78:** `        source = (ROOT / filename).read_text(encoding='utf-8').splitlines()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 79:** `        sections.extend([f'## \`{filename}\`', ''])`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 80:** `        for number, line in enumerate(source, 1):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 81:** `            if not line.strip():`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 82:** `                continue`  
**Para qué sirve:** Salta a la siguiente iteración del ciclo.  

**Línea 83:** `            # El código se escapa como inline code para no romper la tabla.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 84:** `            shown = line.replace('\`', '\\\`').replace('&#124;', '&#124;')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 85:** `            sections.append(f'**Línea {number}:** \`{shown}\`  ')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 86:** `            sections.append(f'**Para qué sirve:** {explain(line)}  ')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 87:** `            sections.append('')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 88:** `    OUTPUT.write_text('\n'.join(sections), encoding='utf-8')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 89:** `    return OUTPUT`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 92:** `if __name__ == '__main__':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 93:** `    print(generate())`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  
