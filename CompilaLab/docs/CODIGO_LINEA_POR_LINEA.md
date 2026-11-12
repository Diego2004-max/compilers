# CompilaLab — Guía de lectura línea por línea

Cada entrada conserva el número real de línea del archivo.
Las explicaciones son ayudas de lectura; las decisiones del algoritmo se estudian también con los tests.

## `compiler.py`

**Línea 1:** `"""CompilaLab: compilador educativo para una CPU virtual de 3 registros."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 2:** `from __future__ import annotations`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 3:** `from dataclasses import dataclass, asdict`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 4:** `from collections import Counter`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 5:** `import re`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 7:** `@dataclass`  
**Para qué sirve:** Genera automáticamente métodos para una clase de datos.  

**Línea 8:** `class Token:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 9:** `    kind: str`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 10:** `    value: str`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 11:** `    line: int`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 12:** `    column: int`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 14:** `class CompileError(Exception):`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 15:** `    def __init__(self, phase, line, column, message):`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 16:** `        super().__init__(f'{phase} (línea {line}, columna {column}): {message}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 17:** `        self.phase, self.line, self.column, self.message = phase, line, column, message`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 19:** `PATTERN = re.compile(r'(?P<COMMENT>//[^\n]*)&#124;(?P<SPACE>[ \t\r]+)&#124;(?P<NEWLINE>\n)&#124;(?P<NUMBER>\d+(?:\.\d+)?)&#124;(?P<STRING>"(?:[^"\\]&#124;\\.)*")&#124;(?P<ID>[a-zA-Z_][\w]*)&#124;(?P<OP>==&#124;!=&#124;<=&#124;>=&#124;[+*/=;(){}<>,-])&#124;(?P<INVALID>.)')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 20:** `KEYWORDS = {'int','float','string','bool','true','false','print','fn','return','new','free'}`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 22:** `def lex(source):`  
**Para qué sirve:** Define la función `lex` y sus parámetros de entrada.  

**Línea 23:** `    tokens=[]; line=1; col=1`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 24:** `    for m in PATTERN.finditer(source):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 25:** `        kind=m.lastgroup; val=m.group()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 26:** `        if kind=='NEWLINE': line+=1; col=1; continue`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 27:** `        if kind in ('SPACE','COMMENT'): col+=len(val); continue`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 28:** `        if kind=='STRING' and '\n' in val: raise CompileError('Léxico',line,col,'Cadena sin cerrar')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 29:** `        if kind=='INVALID': raise CompileError('Léxico',line,col,f'Carácter inválido {val!r}')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 30:** `        if kind=='ID' and val in KEYWORDS: kind=val.upper()`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 31:** `        if kind=='OP': kind=val`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 32:** `        tokens.append(Token(kind,val,line,col)); col+=len(val)`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 33:** `    tokens.append(Token('EOF','',line,col))`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 34:** `    return tokens`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 36:** `@dataclass`  
**Para qué sirve:** Genera automáticamente métodos para una clase de datos.  

**Línea 37:** `class Node:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 38:** `    kind: str`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 39:** `    line: int`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 40:** `    value: object=None`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 41:** `    children: tuple=()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 42:** `    def json(self):`  
**Para qué sirve:** Define la función `json` y sus parámetros de entrada.  

**Línea 43:** `        return {'kind':self.kind,'line':self.line,'value':self.value,'children':[c.json() for c in self.children]}`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 45:** `class Parser:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 46:** `    def __init__(self,tokens): self.ts=tokens; self.i=0`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 47:** `    def at(self,*kinds): return self.ts[self.i].kind in kinds`  
**Para qué sirve:** Define la función `at` y sus parámetros de entrada.  

**Línea 48:** `    def take(self,kind=None):`  
**Para qué sirve:** Define la función `take` y sus parámetros de entrada.  

**Línea 49:** `        t=self.ts[self.i]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 50:** `        if kind and t.kind!=kind: raise CompileError('Sintáctico',t.line,t.column,f'Se esperaba {kind}, llegó {t.value or "fin de archivo"!r}')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 51:** `        self.i+=1; return t`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 52:** `    def parse(self):`  
**Para qué sirve:** Define la función `parse` y sus parámetros de entrada.  

**Línea 53:** `        items=[]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 54:** `        while not self.at('EOF'): items.append(self.statement())`  
**Para qué sirve:** Repite un bloque mientras la condición siga siendo verdadera.  

**Línea 55:** `        return Node('program',1,children=tuple(items))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 56:** `    def statement(self):`  
**Para qué sirve:** Define la función `statement` y sus parámetros de entrada.  

**Línea 57:** `        t=self.ts[self.i]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 58:** `        if self.at('INT','FLOAT','STRING','BOOL'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 59:** `            typ=self.take().value; name=self.take('ID'); self.take('='); exp=self.expr(); self.take(';')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 60:** `            return Node('declare',t.line,{'type':typ,'name':name.value},(exp,))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 61:** `        if self.at('PRINT'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 62:** `            self.take(); self.take('('); exp=self.expr(); self.take(')'); self.take(';')`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 63:** `            return Node('print',t.line,children=(exp,))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 64:** `        if self.at('FREE'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 65:** `            self.take(); self.take('('); name=self.take('ID'); self.take(')'); self.take(';')`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 66:** `            return Node('free',t.line,name.value)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 67:** `        if self.at('FN'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 68:** `            self.take(); name=self.take('ID'); self.take('('); self.take(')'); self.take('{')`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 69:** `            body=[]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 70:** `            while not self.at('}','EOF'): body.append(self.statement())`  
**Para qué sirve:** Repite un bloque mientras la condición siga siendo verdadera.  

**Línea 71:** `            self.take('}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 72:** `            return Node('function',t.line,name.value,tuple(body))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 73:** `        if self.at('RETURN'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 74:** `            self.take(); exp=self.expr(); self.take(';'); return Node('return',t.line,children=(exp,))`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 75:** `        if self.at('ID'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 76:** `            name=self.take();`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 77:** `            if self.at('('):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 78:** `                self.take('('); self.take(')'); self.take(';'); return Node('call',t.line,name.value)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 79:** `            self.take('='); exp=self.expr(); self.take(';'); return Node('assign',t.line,name.value,(exp,))`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 80:** `        raise CompileError('Sintáctico',t.line,t.column,f'Sentencia inesperada {t.value!r}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 81:** `    def expr(self): return self.comparison()`  
**Para qué sirve:** Define la función `expr` y sus parámetros de entrada.  

**Línea 82:** `    def comparison(self):`  
**Para qué sirve:** Define la función `comparison` y sus parámetros de entrada.  

**Línea 83:** `        left=self.add()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 84:** `        while self.at('==','!=','<','>','<=','>='):`  
**Para qué sirve:** Repite un bloque mientras la condición siga siendo verdadera.  

**Línea 85:** `            op=self.take(); left=Node('binary',op.line,op.value,(left,self.add()))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 86:** `        return left`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 87:** `    def add(self):`  
**Para qué sirve:** Define la función `add` y sus parámetros de entrada.  

**Línea 88:** `        left=self.mul()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 89:** `        while self.at('+','-'):`  
**Para qué sirve:** Repite un bloque mientras la condición siga siendo verdadera.  

**Línea 90:** `            op=self.take(); left=Node('binary',op.line,op.value,(left,self.mul()))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 91:** `        return left`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 92:** `    def mul(self):`  
**Para qué sirve:** Define la función `mul` y sus parámetros de entrada.  

**Línea 93:** `        left=self.unary()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 94:** `        while self.at('*','/'):`  
**Para qué sirve:** Repite un bloque mientras la condición siga siendo verdadera.  

**Línea 95:** `            op=self.take(); left=Node('binary',op.line,op.value,(left,self.unary()))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 96:** `        return left`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 97:** `    def unary(self):`  
**Para qué sirve:** Define la función `unary` y sus parámetros de entrada.  

**Línea 98:** `        if self.at('-'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 99:** `            t=self.take(); return Node('binary',t.line,'-', (Node('number',t.line,'0'),self.unary()))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 100:** `        return self.atom()`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 101:** `    def atom(self):`  
**Para qué sirve:** Define la función `atom` y sus parámetros de entrada.  

**Línea 102:** `        t=self.ts[self.i]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 103:** `        if self.at('NUMBER'): self.take(); return Node('number',t.line,t.value)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 104:** `        if self.at('STRING'): self.take(); return Node('string',t.line,t.value[1:-1])`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 105:** `        if self.at('TRUE','FALSE'): self.take(); return Node('boolean',t.line,t.value=='true')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 106:** `        if self.at('ID'): self.take(); return Node('variable',t.line,t.value)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 107:** `        if self.at('NEW'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 108:** `            self.take(); self.take('('); size=self.take('NUMBER'); self.take(')')`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 109:** `            if '.' in size.value or int(size.value)<=0: raise CompileError('Sintáctico',t.line,t.column,'new requiere un entero positivo')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 110:** `            return Node('new',t.line,int(size.value))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 111:** `        if self.at('('): self.take(); exp=self.expr(); self.take(')'); return exp`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 112:** `        raise CompileError('Sintáctico',t.line,t.column,f'Expresión inesperada {t.value!r}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 114:** `class Semantic:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 115:** `    def __init__(self): self.scopes=[{}]; self.symbols=[]; self.functions={}`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 116:** `    def lookup(self,name,line):`  
**Para qué sirve:** Define la función `lookup` y sus parámetros de entrada.  

**Línea 117:** `        for scope in reversed(self.scopes):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 118:** `            if name in scope: return scope[name]`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 119:** `        raise CompileError('Semántico',line,1,f'Variable {name!r} no declarada')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 120:** `    def expr(self,n):`  
**Para qué sirve:** Define la función `expr` y sus parámetros de entrada.  

**Línea 121:** `        if n.kind=='number': return 'float' if '.' in n.value else 'int'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 122:** `        if n.kind=='string': return 'string'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 123:** `        if n.kind=='boolean': return 'bool'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 124:** `        if n.kind=='new': return 'ptr'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 125:** `        if n.kind=='variable': return self.lookup(n.value,n.line)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 126:** `        if n.kind=='binary':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 127:** `            a,b=(self.expr(c) for c in n.children)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 128:** `            if n.value in ('==','!=','<','>','<=','>='):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 129:** `                if a!=b and not ({a,b}<={'int','float'}): raise CompileError('Semántico',n.line,1,'Comparación de tipos incompatibles')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 130:** `                return 'bool'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 131:** `            if a not in ('int','float') or b not in ('int','float'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 132:** `                raise CompileError('Semántico',n.line,1,f'Operación {n.value} inválida entre {a} y {b}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 133:** `            return 'float' if 'float' in (a,b) or n.value=='/' else 'int'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 134:** `        raise ValueError(n.kind)`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 135:** `    def check(self,root):`  
**Para qué sirve:** Define la función `check` y sus parámetros de entrada.  

**Línea 136:** `        for stmt in root.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 137:** `            if stmt.kind=='function':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 138:** `                if stmt.value in self.functions: raise CompileError('Semántico',stmt.line,1,'Función duplicada')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 139:** `                self.functions[stmt.value]=stmt`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 140:** `        for stmt in root.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 141:** `            if stmt.kind=='function':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 142:** `                self.scopes.append({}); self.block(stmt.children,stmt.value); self.scopes.pop()`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 143:** `            else: self.block((stmt,),'global')`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 144:** `        return self.symbols`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 145:** `    def block(self,statements,scope):`  
**Para qué sirve:** Define la función `block` y sus parámetros de entrada.  

**Línea 146:** `        for s in statements:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 147:** `            if s.kind=='declare':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 148:** `                name=s.value['name']; typ=s.value['type']; found=self.expr(s.children[0]); actual='int' if typ=='int' and found=='ptr' else found`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 149:** `                if name in self.scopes[-1]: raise CompileError('Semántico',s.line,1,f'Declaración duplicada: {name}')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 150:** `                if typ!=actual and not (typ=='float' and actual=='int'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 151:** `                    raise CompileError('Semántico',s.line,1,f'{name}: se esperaba {typ}, llegó {found}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 152:** `                self.scopes[-1][name]=typ; self.symbols.append({'name':name,'type':typ,'scope':scope,'line':s.line})`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 153:** `            elif s.kind=='assign':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 154:** `                expected=self.lookup(s.value,s.line); actual=self.expr(s.children[0]); actual='int' if expected=='int' and actual=='ptr' else actual`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 155:** `                if expected!=actual and not (expected=='float' and actual=='int'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 156:** `                    raise CompileError('Semántico',s.line,1,f'{s.value}: se esperaba {expected}, llegó {actual}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 157:** `            elif s.kind in ('print','return'): self.expr(s.children[0])`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 158:** `            elif s.kind=='free': self.lookup(s.value,s.line)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 159:** `            elif s.kind=='call':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 160:** `                if s.value not in self.functions: raise CompileError('Semántico',s.line,1,f'Función {s.value} no declarada')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 162:** `@dataclass`  
**Para qué sirve:** Genera automáticamente métodos para una clase de datos.  

**Línea 163:** `class Quad:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 164:** `    op: str`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 165:** `    a: object=None`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 166:** `    b: object=None`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 167:** `    dest: object=None`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 168:** `    line: int=0`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 169:** `    def show(self):`  
**Para qué sirve:** Define la función `show` y sus parámetros de entrada.  

**Línea 170:** `        if self.op=='CONST': return f'{self.dest} = {self.a!r}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 171:** `        if self.op=='MOV': return f'{self.dest} = {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 172:** `        if self.op=='BIN': return f'{self.dest} = {self.a} {self.b[0]} {self.b[1]}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 173:** `        if self.op=='PRINT': return f'print {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 174:** `        if self.op=='ALLOC': return f'{self.dest} = alloc {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 175:** `        if self.op=='FREE': return f'free {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 176:** `        if self.op=='ENTER': return f'enter {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 177:** `        if self.op=='LEAVE': return f'leave {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 178:** `        if self.op=='CALL': return f'call {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 179:** `        if self.op=='RET': return f'return {self.a}'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 180:** `        return str(self)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 182:** `class IRBuilder:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 183:** `    def __init__(self): self.quads=[]; self.index=0`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 184:** `    def emit(self,*args): self.quads.append(Quad(*args))`  
**Para qué sirve:** Define la función `emit` y sus parámetros de entrada.  

**Línea 185:** `    def tmp(self): self.index+=1; return f't{self.index}'`  
**Para qué sirve:** Define la función `tmp` y sus parámetros de entrada.  

**Línea 186:** `    def expr(self,n):`  
**Para qué sirve:** Define la función `expr` y sus parámetros de entrada.  

**Línea 187:** `        if n.kind in ('number','string','boolean'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 188:** `            t=self.tmp(); v=float(n.value) if n.kind=='number' and '.' in n.value else int(n.value) if n.kind=='number' else n.value`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 189:** `            self.emit('CONST',v,None,t,n.line); return t`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 190:** `        if n.kind=='variable': return n.value`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 191:** `        if n.kind=='new':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 192:** `            t=self.tmp(); self.emit('ALLOC',n.value,None,t,n.line); return t`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 193:** `        if n.kind=='binary':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 194:** `            left=self.expr(n.children[0]); right=self.expr(n.children[1]); t=self.tmp()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 195:** `            self.emit('BIN',left,(n.value,right),t,n.line); return t`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 196:** `        raise ValueError(n.kind)`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 197:** `    def statement(self,s):`  
**Para qué sirve:** Define la función `statement` y sus parámetros de entrada.  

**Línea 198:** `        if s.kind in ('declare','assign'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 199:** `            dst=s.value['name'] if s.kind=='declare' else s.value`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 200:** `            src=self.expr(s.children[0]); self.emit('MOV',src,None,dst,s.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 201:** `        elif s.kind=='print': self.emit('PRINT',self.expr(s.children[0]),None,None,s.line)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 202:** `        elif s.kind=='free': self.emit('FREE',s.value,None,None,s.line)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 203:** `        elif s.kind=='call': self.emit('CALL',s.value,None,None,s.line)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 204:** `        elif s.kind=='return': self.emit('RET',self.expr(s.children[0]),None,None,s.line)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 205:** `    def build(self,root):`  
**Para qué sirve:** Define la función `build` y sus parámetros de entrada.  

**Línea 206:** `        funcs={s.value:s for s in root.children if s.kind=='function'}`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 207:** `        self.emit('ENTER','main',None,None,1)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 208:** `        for s in root.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 209:** `            if s.kind!='function': self.statement(s)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 210:** `        self.emit('LEAVE','main',None,None,root.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 211:** `        for name,fn in funcs.items():`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 212:** `            self.emit('ENTER',name,None,None,fn.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 213:** `            for s in fn.children: self.statement(s)`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 214:** `            self.emit('LEAVE',name,None,None,fn.line)`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 215:** `        return self.quads`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 217:** `def calculate(op,a,b):`  
**Para qué sirve:** Define la función `calculate` y sus parámetros de entrada.  

**Línea 218:** `    if op=='+': return a+b`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 219:** `    if op=='-': return a-b`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 220:** `    if op=='*': return a*b`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 221:** `    if op=='/':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 222:** `        if b==0: raise ZeroDivisionError('División por cero')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 223:** `        return a/b`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 224:** `    return {'==':lambda:a==b,'!=':lambda:a!=b,'<':lambda:a<b,'>':lambda:a>b,'<=':lambda:a<=b,'>=':lambda:a>=b}[op]()`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 226:** `def eliminate_dead_temporaries(quads):`  
**Para qué sirve:** Define la función `eliminate_dead_temporaries` y sus parámetros de entrada.  

**Línea 227:** `    """DCE conservador: elimina definiciones puras de temporales tN sin usos.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 229:** `    No elimina asignaciones de usuario, llamadas, prints ni operaciones de memoria.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 230:** `    """`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 231:** `    live=set(); kept=[]; notes=[]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 232:** `    for q in reversed(quads):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 233:** `        if q.op in ('CONST','MOV','BIN') and isinstance(q.dest,str) and re.fullmatch(r't\d+',q.dest) and q.dest not in live:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 234:** `            notes.append(f'Línea {q.line}: temporal muerto {q.dest} eliminado')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 235:** `            continue`  
**Para qué sirve:** Salta a la siguiente iteración del ciclo.  

**Línea 236:** `        if q.dest is not None and q.op in ('CONST','MOV','BIN','ALLOC'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 237:** `            live.discard(q.dest)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 238:** `        if q.op=='BIN': live.add(q.a); live.add(q.b[1])`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 239:** `        elif q.op in ('MOV','PRINT','FREE','RET') and isinstance(q.a,str): live.add(q.a)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 240:** `        kept.append(q)`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 241:** `    return list(reversed(kept)),list(reversed(notes))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 243:** `def optimize(quads):`  
**Para qué sirve:** Define la función `optimize` y sus parámetros de entrada.  

**Línea 244:** `    # Propagación de constantes y plegado, sin borrar instrucciones con efectos.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 245:** `    known={}; out=[]; notes=[]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 246:** `    for q in quads:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 247:** `        if q.op=='ENTER': known={}`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 248:** `        if q.op=='CONST': known[q.dest]=q.a`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 249:** `        elif q.op=='MOV':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 250:** `            if q.a in known:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 251:** `                value=known[q.a]; q=Quad('CONST',value,None,q.dest,q.line); known[q.dest]=value; notes.append(f'Línea {q.line}: propagación de constante a {q.dest}')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 252:** `            else: known.pop(q.dest,None)`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 253:** `        elif q.op=='BIN':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 254:** `            op,right=q.b`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 255:** `            if q.a in known and right in known:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 256:** `                try:`  
**Para qué sirve:** Inicia un bloque que puede producir excepciones controladas.  

**Línea 257:** `                    v=calculate(op,known[q.a],known[right]); q=Quad('CONST',v,None,q.dest,q.line)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 258:** `                    known[q.dest]=v; notes.append(f'Línea {q.line}: plegado constante en {q.dest}')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 259:** `                except ZeroDivisionError: known.pop(q.dest,None)`  
**Para qué sirve:** Captura un error y permite manejarlo sin terminar abruptamente.  

**Línea 260:** `            else: known.pop(q.dest,None)`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 261:** `        elif q.op in ('CALL','LEAVE'): known={}`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 262:** `        out.append(q)`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 263:** `    # En este lenguaje, DCE de temporales es seguro en programas sin llamadas:`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 264:** `    # las funciones pueden compartir nombres de temporales y requieren un CFG.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 265:** `    if not any(q.op in ('CALL','RET') for q in out):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 266:** `        out,dead_notes=eliminate_dead_temporaries(out)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 267:** `        notes.extend(dead_notes)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 268:** `    return out,notes`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 270:** `class Memory:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 271:** `    def __init__(self): self.stack=[]; self.heap={}; self.next_addr=0x1000; self.events=[]`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 272:** `    def push(self,name): self.stack.append({'function':name,'locals':{}}); self.events.append(f'PUSH frame {name}')`  
**Para qué sirve:** Define la función `push` y sus parámetros de entrada.  

**Línea 273:** `    def pop(self):`  
**Para qué sirve:** Define la función `pop` y sus parámetros de entrada.  

**Línea 274:** `        if not self.stack: raise RuntimeError('Stack underflow')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 275:** `        name=self.stack.pop()['function']; self.events.append(f'POP frame {name}')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 276:** `    def alloc(self,size):`  
**Para qué sirve:** Define la función `alloc` y sus parámetros de entrada.  

**Línea 277:** `        addr=self.next_addr; self.next_addr+=size; self.heap[addr]=size; self.events.append(f'HEAP ALLOC {size} bytes en {hex(addr)}'); return addr`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 278:** `    def free(self,addr):`  
**Para qué sirve:** Define la función `free` y sus parámetros de entrada.  

**Línea 279:** `        if addr not in self.heap: raise RuntimeError(f'Doble free o puntero inválido: {hex(addr)}')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 280:** `        del self.heap[addr]; self.events.append(f'HEAP FREE {hex(addr)}')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 282:** `class Backend:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 283:** `    """Emite ensamblador para una ISA virtual; tres registros y spill explícito."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 284:** `    def __init__(self,registers=3):`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 285:** `        if registers < 3: raise ValueError('Se requieren al menos 3 registros para esta ISA de tres operandos')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 286:** `        self.regs=[f'R{i}' for i in range(registers)]; self.owners={}; self.locations={}; self.asm=[]; self.events=[]; self.spills=0; self.slots={}; self.slot=0`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 287:** `    def emit(self,s): self.asm.append(s)`  
**Para qué sirve:** Define la función `emit` y sus parámetros de entrada.  

**Línea 288:** `    def uses(self,q):`  
**Para qué sirve:** Define la función `uses` y sus parámetros de entrada.  

**Línea 289:** `        if q.op=='BIN': return [q.a,q.b[1]]`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 290:** `        if q.op in ('MOV','PRINT','FREE','RET'): return [q.a]`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 291:** `        return []`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 292:** `    def future(self,quads,i):`  
**Para qué sirve:** Define la función `future` y sus parámetros de entrada.  

**Línea 293:** `        return Counter(x for q in quads[i+1:] for x in self.uses(q) if isinstance(x,str))`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 294:** `    def reg(self,name,quads,i,protect=()):`  
**Para qué sirve:** Define la función `reg` y sus parámetros de entrada.  

**Línea 295:** `        if name in self.locations: return self.locations[name]`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 296:** `        free=next((r for r in self.regs if r not in self.owners),None)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 297:** `        if free is None:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 298:** `            counts=self.future(quads,i)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 299:** `            candidates=[(counts.get(v,0),r,v) for r,v in self.owners.items() if v not in protect]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 300:** `            if not candidates: raise RuntimeError('No hay registro libre para los operandos; aumente el pool')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 301:** `            _,free,victim=min(candidates)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 302:** `            if counts.get(victim,0):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 303:** `                if victim not in self.slots: self.slots[victim]=0x2000+self.slot*8; self.slot+=1`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 304:** `                self.emit(f'STORE [{hex(self.slots[victim])}], {free} ; SPILL {victim}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 305:** `                self.events.append(f'SPILL {victim}: {free} → STACK[{hex(self.slots[victim])}]'); self.spills+=1`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 306:** `            self.locations.pop(victim,None); self.owners.pop(free)`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 307:** `        self.owners[free]=name; self.locations[name]=free`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 308:** `        if name in self.slots:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 309:** `            self.emit(f'LOAD {free}, [{hex(self.slots[name])}] ; RECARGA {name}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 310:** `            self.events.append(f'RELOAD {name}: STACK → {free}')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 311:** `        return free`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 312:** `    def release_dead(self,quads,i):`  
**Para qué sirve:** Define la función `release_dead` y sus parámetros de entrada.  

**Línea 313:** `        future=self.future(quads,i)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 314:** `        for reg,name in list(self.owners.items()):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 315:** `            if not future.get(name,0): self.owners.pop(reg); self.locations.pop(name,None)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 316:** `    def generate(self,quads):`  
**Para qué sirve:** Define la función `generate` y sus parámetros de entrada.  

**Línea 317:** `        for i,q in enumerate(quads):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 318:** `            if q.op in ('ENTER','LEAVE','CALL'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 319:** `                if q.op=='CALL':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 320:** `                    future=self.future(quads,i)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 321:** `                    for register,name in list(self.owners.items()):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 322:** `                        if future.get(name,0):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 323:** `                            if name not in self.slots:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 324:** `                                self.slots[name]=0x2000+self.slot*8; self.slot+=1`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 325:** `                            self.emit(f'STORE [{hex(self.slots[name])}], {register} ; CONSERVAR {name} ANTES DE CALL')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 326:** `                            self.events.append(f'CALL-SAVE {name}: {register} → STACK[{hex(self.slots[name])}]')`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 327:** `                self.emit(f'{q.op} {q.a}'); self.owners.clear(); self.locations.clear()`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 328:** `            elif q.op=='CONST':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 329:** `                r=self.reg(q.dest,quads,i); self.emit(f'LI {r}, {q.a!r} ; {q.dest}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 330:** `            elif q.op=='MOV':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 331:** `                source=self.reg(q.a,quads,i); dest=self.reg(q.dest,quads,i,protect=(q.a,))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 332:** `                self.emit(f'MOV {dest}, {source} ; {q.dest}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 333:** `            elif q.op=='BIN':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 334:** `                op,right=q.b; leftreg=self.reg(q.a,quads,i)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 335:** `                rightreg=self.reg(right,quads,i,protect=(q.a,))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 336:** `                dest=self.reg(q.dest,quads,i,protect=(q.a,right))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 337:** `                self.emit(f'{ {"+":"ADD","-":"SUB","*":"MUL","/":"DIV","==":"EQ","!=":"NE","<":"LT",">":"GT","<=":"LE",">=":"GE"}[op]} {dest}, {leftreg}, {rightreg} ; {q.dest}')`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 338:** `            elif q.op=='PRINT':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 339:** `                r=self.reg(q.a,quads,i); self.emit(f'PRINT {r}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 340:** `            elif q.op=='ALLOC':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 341:** `                r=self.reg(q.dest,quads,i); self.emit(f'ALLOC {r}, {q.a}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 342:** `            elif q.op=='FREE':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 343:** `                r=self.reg(q.a,quads,i); self.emit(f'FREE {r}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 344:** `            elif q.op=='RET':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 345:** `                r=self.reg(q.a,quads,i); self.emit(f'RET {r}')`  
**Para qué sirve:** Emite una instrucción o un registro para una fase posterior.  

**Línea 346:** `            self.release_dead(quads,i)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 347:** `        return self.asm`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 349:** `class Interpreter:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 350:** `    """Ejecuta TAC y simula Stack/Heap; no ejecuta ensamblador nativo."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 351:** `    def __init__(self,quads): self.qs=quads; self.memory=Memory(); self.output=[]; self.globals={}; self.locals={}; self.calls={}; self.return_value=None`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 352:** `    def val(self,k):`  
**Para qué sirve:** Define la función `val` y sus parámetros de entrada.  

**Línea 353:** `        if k in self.locals: return self.locals[k]`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 354:** `        if k in self.globals: return self.globals[k]`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 355:** `        raise RuntimeError(f'Variable temporal no inicializada: {k}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 356:** `    def execute(self):`  
**Para qué sirve:** Define la función `execute` y sus parámetros de entrada.  

**Línea 357:** `        entries={q.a:i for i,q in enumerate(self.qs) if q.op=='ENTER'}`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 358:** `        self.memory.push('main'); self.locals={}; pc=entries['main']+1; steps=0`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 359:** `        while pc<len(self.qs):`  
**Para qué sirve:** Repite un bloque mientras la condición siga siendo verdadera.  

**Línea 360:** `            steps+=1`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 361:** `            if steps>10000: raise RuntimeError('Límite de ejecución alcanzado')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 362:** `            q=self.qs[pc]; op=q.op`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 363:** `            if op=='CONST': self.locals[q.dest]=q.a`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 364:** `            elif op=='MOV':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 365:** `                v=self.val(q.a); self.locals[q.dest]=v`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 366:** `                if len(self.memory.stack)==1: self.globals[q.dest]=v`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 367:** `                self.memory.stack[-1]['locals'][q.dest]=v`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 368:** `            elif op=='BIN': self.locals[q.dest]=calculate(q.b[0],self.val(q.a),self.val(q.b[1]))`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 369:** `            elif op=='PRINT': self.output.append(str(self.val(q.a)))`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 370:** `            elif op=='ALLOC': self.locals[q.dest]=self.memory.alloc(q.a)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 371:** `            elif op=='FREE': self.memory.free(self.val(q.a))`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 372:** `            elif op=='CALL':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 373:** `                if q.a not in entries: raise RuntimeError(f'Función no encontrada: {q.a}')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 374:** `                self.calls[len(self.memory.stack)]=(pc+1,self.locals)`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 375:** `                self.memory.push(q.a); self.locals={}; pc=entries[q.a]+1; continue`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 376:** `            elif op in ('LEAVE','RET'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 377:** `                if op=='RET': self.return_value=self.val(q.a)`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 378:** `                self.memory.pop()`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 379:** `                if not self.memory.stack: break`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 380:** `                pc,self.locals=self.calls.pop(len(self.memory.stack)); continue`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 381:** `            pc+=1`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 382:** `        return self.output`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 384:** `def compile_source(source,registers=3,optimized=False,run=True):`  
**Para qué sirve:** Define la función `compile_source` y sus parámetros de entrada.  

**Línea 385:** `    result={'source':source,'error':None}`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 386:** `    try:`  
**Para qué sirve:** Inicia un bloque que puede producir excepciones controladas.  

**Línea 387:** `        ts=lex(source); result['tokens']=[asdict(t) for t in ts]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 388:** `        from automata import analyze_automata, GRAMMAR`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 389:** `        result['automata']=analyze_automata(ts); result['grammar']=GRAMMAR`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 390:** `        ast=Parser(ts).parse(); result['ast']=ast.json()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 391:** `        semantic=Semantic(); result['symbols']=semantic.check(ast)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 392:** `        raw=IRBuilder().build(ast); result['tac']=[q.show() for q in raw]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 393:** `        opt,notes=optimize([Quad(**asdict(q)) for q in raw]); result['optimized_tac']=[q.show() for q in opt]; result['optimizations']=notes`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 394:** `        chosen=opt if optimized else raw`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 395:** `        result['quads']=[asdict(q) for q in chosen]`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 396:** `        backend=Backend(registers); result['assembly']=backend.generate(chosen); result['register_events']=backend.events; result['spill_count']=backend.spills`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 397:** `        result['register_slots']={name:hex(addr) for name,addr in backend.slots.items()}`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 398:** `        if run:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 399:** `            vm=Interpreter(chosen); result['output']=vm.execute(); result['memory_events']=vm.memory.events; result['globals']=vm.globals; result['heap_remaining']=vm.memory.heap`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 400:** `            from virtual_cpu import VirtualCPU`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 401:** `            cpu=VirtualCPU(result['assembly'], registers); result['cpu_output']=cpu.execute()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 402:** `            result['cpu_trace']=cpu.trace; result['cpu_registers']=cpu.registers`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 403:** `            result['cpu_ram']={hex(k):v for k,v in cpu.ram.items()}`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 404:** `            result['cpu_memory_events']=cpu.memory.events`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 405:** `            result['cpu_heap_remaining']={hex(k):v for k,v in cpu.memory.heap.items()}`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 406:** `            result['cpu_matches_tac']=(result['cpu_output']==result['output'])`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 407:** `            if not result['cpu_matches_tac']: raise RuntimeError(f'Diferencia entre TAC {result["output"]} y CPU {result["cpu_output"]}')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 408:** `        result['success']=True`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 409:** `    except (CompileError,RuntimeError,ZeroDivisionError,TypeError,ValueError) as e:`  
**Para qué sirve:** Captura un error y permite manejarlo sin terminar abruptamente.  

**Línea 410:** `        result['success']=False; result['error']=str(e)`  
**Para qué sirve:** Guarda información de una fase en el resultado de compilación.  

**Línea 411:** `    return result`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

## `automata.py`

**Línea 1:** `"""AFD didáctico para identificadores y números; la tokenización principal usa Regex.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 3:** `Las transiciones se exponen para estudiar estados, alfabeto y aceptación.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 4:** `"""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 5:** `from dataclasses import dataclass`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 7:** `@dataclass`  
**Para qué sirve:** Genera automáticamente métodos para una clase de datos.  

**Línea 8:** `class DFAResult:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 9:** `    accepted: bool`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 10:** `    state: str`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 11:** `    trace: list`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 13:** `def identifier_dfa(word):`  
**Para qué sirve:** Define la función `identifier_dfa` y sus parámetros de entrada.  

**Línea 14:** `    state='q0'; trace=[]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 15:** `    for ch in word:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 16:** `        if state=='q0': nxt='q1' if ch.isascii() and (ch.isalpha() or ch=='_') else 'ERROR'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 17:** `        elif state=='q1': nxt='q1' if ch.isascii() and (ch.isalnum() or ch=='_') else 'ERROR'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 18:** `        else: nxt='ERROR'`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 19:** `        trace.append({'caracter':ch,'desde':state,'hasta':nxt}); state=nxt`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 20:** `    return DFAResult(state=='q1',state,trace)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 22:** `def number_dfa(word):`  
**Para qué sirve:** Define la función `number_dfa` y sus parámetros de entrada.  

**Línea 23:** `    state='q0'; trace=[]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 24:** `    for ch in word:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 25:** `        if state=='q0': nxt='entero' if ch.isdigit() and ch.isascii() else 'ERROR'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 26:** `        elif state=='entero': nxt='entero' if ch.isdigit() and ch.isascii() else 'punto' if ch=='.' else 'ERROR'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 27:** `        elif state=='punto': nxt='decimal' if ch.isdigit() and ch.isascii() else 'ERROR'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 28:** `        elif state=='decimal': nxt='decimal' if ch.isdigit() and ch.isascii() else 'ERROR'`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 29:** `        else: nxt='ERROR'`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 30:** `        trace.append({'caracter':ch,'desde':state,'hasta':nxt}); state=nxt`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 31:** `    return DFAResult(state in ('entero','decimal'),state,trace)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 33:** `def analyze_automata(tokens):`  
**Para qué sirve:** Define la función `analyze_automata` y sus parámetros de entrada.  

**Línea 34:** `    output=[]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 35:** `    for t in tokens:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 36:** `        if t.kind in ('ID','NUMBER'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 37:** `            dfa=identifier_dfa(t.value) if t.kind=='ID' else number_dfa(t.value)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 38:** `            output.append({'lexema':t.value,'tipo':t.kind,'aceptado':dfa.accepted,'estado_final':dfa.state,'transiciones':dfa.trace})`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 39:** `    return output`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 41:** `GRAMMAR = '''program     -> statement* EOF`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 42:** `statement   -> TYPE ID '=' expr ';'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 43:** `             &#124; ID '=' expr ';' &#124; 'print' '(' expr ')' ';'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 44:** `             &#124; 'free' '(' ID ')' ';' &#124; ID '(' ')' ';'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 45:** `             &#124; 'fn' ID '(' ')' '{' statement* '}'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 46:** `             &#124; 'return' expr ';'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 47:** `expr        -> comparison`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 48:** `comparison  -> addition (('=='&#124;'!='&#124;'<'&#124;'>'&#124;'<='&#124;'>=') addition)*`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 49:** `addition    -> multiply (('+'&#124;'-') multiply)*`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 50:** `multiply    -> unary (('*'&#124;'/') unary)*`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 51:** `unary       -> '-' unary &#124; atom`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 52:** `atom        -> NUMBER &#124; STRING &#124; 'true' &#124; 'false' &#124; ID`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 53:** `             &#124; 'new' '(' NUMBER ')' &#124; '(' expr ')'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 54:** `TYPE        -> 'int' &#124; 'float' &#124; 'string' &#124; 'bool'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 55:** `'''`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

## `virtual_cpu.py`

**Línea 1:** `"""CPU virtual: ejecuta la ISA textual generada por CompilaLab.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 3:** `Los registros son un banco limitado, las direcciones de spill viven en RAM,`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 4:** `y ENTER/LEAVE modelan marcos de ejecución (no instrucciones x86).`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 5:** `"""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 6:** `import ast`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 7:** `import re`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 9:** `from compiler import Memory, calculate`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 11:** `class VirtualCPU:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 12:** `    def __init__(self, assembly, register_count=3):`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 13:** `        self.instructions = list(assembly)`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 14:** `        self.registers = {f'R{i}': None for i in range(register_count)}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 15:** `        self.ram = {}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 16:** `        self.memory = Memory()`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 17:** `        self.output = []`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 18:** `        self.trace = []`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 19:** `        self.pc = 0`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 20:** `        self.calls = []`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 21:** `        self.labels = {}`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 22:** `        for index, raw in enumerate(self.instructions):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 23:** `            instruction = raw.split(';', 1)[0].strip()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 24:** `            if instruction.startswith('ENTER '):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 25:** `                self.labels[instruction.split()[1]] = index`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 27:** `    def register(self, name):`  
**Para qué sirve:** Define la función `register` y sus parámetros de entrada.  

**Línea 28:** `        if name not in self.registers:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 29:** `            raise RuntimeError(f'Registro desconocido: {name}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 30:** `        value = self.registers[name]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 31:** `        if value is None:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 32:** `            raise RuntimeError(f'Lectura de registro no inicializado: {name} (PC={self.pc})')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 33:** `        return value`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 35:** `    def execute(self):`  
**Para qué sirve:** Define la función `execute` y sus parámetros de entrada.  

**Línea 36:** `        if 'main' not in self.labels:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 37:** `            raise RuntimeError('No existe punto de entrada main')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 38:** `        self.pc = self.labels['main']`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 39:** `        steps = 0`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 40:** `        while self.pc < len(self.instructions):`  
**Para qué sirve:** Repite un bloque mientras la condición siga siendo verdadera.  

**Línea 41:** `            steps += 1`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 42:** `            if steps > 10000:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 43:** `                raise RuntimeError('CPU: límite de 10000 instrucciones')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 44:** `            raw = self.instructions[self.pc]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 45:** `            instruction = raw.split(';', 1)[0].strip()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 46:** `            if not instruction:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 47:** `                self.pc += 1`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 48:** `                continue`  
**Para qué sirve:** Salta a la siguiente iteración del ciclo.  

**Línea 49:** `            op, _, rest = instruction.partition(' ')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 50:** `            args = [arg.strip() for arg in rest.split(',')] if rest else []`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 51:** `            before = self.pc`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 52:** `            jump = None`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 53:** `            if op == 'ENTER':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 54:** `                self.memory.push(args[0])`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 55:** `            elif op == 'LEAVE':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 56:** `                self.memory.pop()`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 57:** `                if not self.calls:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 58:** `                    self.trace.append({'pc': before, 'instruction': instruction, 'registers': dict(self.registers), 'ram': {hex(k):v for k,v in self.ram.items()}, 'stack': [f['function'] for f in self.memory.stack], 'heap': {hex(k):v for k,v in self.memory.heap.items()}})`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 59:** `                    break`  
**Para qué sirve:** Termina el ciclo actual.  

**Línea 60:** `                jump = self.calls.pop()`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 61:** `            elif op == 'CALL':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 62:** `                if args[0] not in self.labels:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 63:** `                    raise RuntimeError(f'CPU: función no encontrada: {args[0]}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 64:** `                self.calls.append(self.pc + 1)`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 65:** `                jump = self.labels[args[0]]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 66:** `            elif op == 'RET':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 67:** `                self.memory.pop()`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 68:** `                if not self.calls:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 69:** `                    raise RuntimeError('CPU: RET sin llamada')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 70:** `                jump = self.calls.pop()`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 71:** `            elif op == 'LI':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 72:** `                self.registers[args[0]] = ast.literal_eval(args[1])`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 73:** `            elif op == 'MOV':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 74:** `                self.registers[args[0]] = self.register(args[1])`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 75:** `            elif op == 'STORE':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 76:** `                match = re.fullmatch(r'\[(0x[0-9a-fA-F]+)\]', args[0])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 77:** `                if not match:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 78:** `                    raise RuntimeError(f'CPU: dirección inválida {args[0]}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 79:** `                self.ram[int(match.group(1), 16)] = self.register(args[1])`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 80:** `            elif op == 'LOAD':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 81:** `                match = re.fullmatch(r'\[(0x[0-9a-fA-F]+)\]', args[1])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 82:** `                if not match:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 83:** `                    raise RuntimeError(f'CPU: dirección inválida {args[1]}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 84:** `                addr = int(match.group(1), 16)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 85:** `                if addr not in self.ram:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 86:** `                    raise RuntimeError(f'CPU: lectura de RAM no inicializada: {hex(addr)}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 87:** `                self.registers[args[0]] = self.ram[addr]`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 88:** `            elif op in ('ADD', 'SUB', 'MUL', 'DIV', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 89:** `                symbol = {'ADD': '+', 'SUB': '-', 'MUL': '*', 'DIV': '/',`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 90:** `                          'EQ': '==', 'NE': '!=', 'LT': '<', 'GT': '>', 'LE': '<=', 'GE': '>='}[op]`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 91:** `                self.registers[args[0]] = calculate(symbol, self.register(args[1]), self.register(args[2]))`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 92:** `            elif op == 'PRINT':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 93:** `                self.output.append(str(self.register(args[0])))`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 94:** `            elif op == 'ALLOC':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 95:** `                self.registers[args[0]] = self.memory.alloc(int(args[1]))`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 96:** `            elif op == 'FREE':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 97:** `                self.memory.free(self.register(args[0]))`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 98:** `            else:`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 99:** `                raise RuntimeError(f'CPU: instrucción desconocida: {instruction}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 100:** `            self.trace.append({'pc': before, 'instruction': instruction, 'registers': dict(self.registers), 'ram': {hex(k):v for k,v in self.ram.items()}, 'stack': [f['function'] for f in self.memory.stack], 'heap': {hex(k):v for k,v in self.memory.heap.items()}})`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 101:** `            self.pc = jump if jump is not None else self.pc + 1`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 102:** `        return self.output`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

## `native_backend.py`

**Línea 1:** `"""Backend nativo: traduce el AST validado a C11 y lo compila con GCC o Clang.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 3:** `El resultado es un ejecutable de máquina REAL, no una CPU simulada.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 4:** `La selección de registros físicos corresponde al compilador C instalado.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 5:** `"""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 6:** `from __future__ import annotations`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 7:** `import os`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 8:** `from pathlib import Path`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 9:** `import shutil`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 10:** `import subprocess`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 11:** `import tempfile`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 12:** `from dataclasses import dataclass`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 15:** `class NativeError(Exception):`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 16:** `    """Error de traducción, compilación o ejecución nativa."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 19:** `def c_string(value):`  
**Para qué sirve:** Define la función `c_string` y sus parámetros de entrada.  

**Línea 20:** `    """Escapa una cadena para convertirla en un literal C válido."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 21:** `    import json`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 22:** `    return json.dumps(value, ensure_ascii=True)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 25:** `class CEmitter:`  
**Para qué sirve:** Declara una clase y define la responsabilidad de sus objetos.  

**Línea 26:** `    """Genera C11 desde el AST de CompilaLab, respetando sus tipos y ámbitos."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 27:** `    def __init__(self):`  
**Para qué sirve:** Define la función `__init__` y sus parámetros de entrada.  

**Línea 28:** `        self.types = [{}]`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 29:** `        self.indent = 0`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 30:** `        self.lines = []`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 32:** `    def write(self, statement):`  
**Para qué sirve:** Define la función `write` y sus parámetros de entrada.  

**Línea 33:** `        self.lines.append('    ' * self.indent + statement)`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 35:** `    def lookup(self, name):`  
**Para qué sirve:** Define la función `lookup` y sus parámetros de entrada.  

**Línea 36:** `        for scope in reversed(self.types):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 37:** `            if name in scope:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 38:** `                return scope[name]`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 39:** `        raise NativeError(f'Variable no declarada: {name}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 41:** `    def expression(self, node):`  
**Para qué sirve:** Define la función `expression` y sus parámetros de entrada.  

**Línea 42:** `        if node.kind == 'number':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 43:** `            return node.value`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 44:** `        if node.kind == 'string':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 45:** `            return c_string(node.value)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 46:** `        if node.kind == 'boolean':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 47:** `            return 'true' if node.value else 'false'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 48:** `        if node.kind == 'variable':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 49:** `            return node.value`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 50:** `        if node.kind == 'binary':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 51:** `            left, right = node.children`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 52:** `            if node.value == '/':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 53:** `                # CompilaLab define división real incluso para dos enteros.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 54:** `                return f'((double)({self.expression(left)}) / (double)({self.expression(right)}))'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 55:** `            if self.infer(left) == 'string' and self.infer(right) == 'string' and node.value in ('==', '!='):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 56:** `                test = '== 0' if node.value == '==' else '!= 0'`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 57:** `                return f'(strcmp({self.expression(left)}, {self.expression(right)}) {test})'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 58:** `            return f'({self.expression(left)} {node.value} {self.expression(right)})'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 59:** `        if node.kind == 'new':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 60:** `            raise NativeError('new/free requieren gestión segura de memoria; no se traducen todavía al backend nativo')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 61:** `        raise NativeError(f'Expresión nativa no soportada: {node.kind}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 63:** `    def infer(self, node):`  
**Para qué sirve:** Define la función `infer` y sus parámetros de entrada.  

**Línea 64:** `        if node.kind == 'number':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 65:** `            return 'float' if '.' in node.value else 'int'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 66:** `        if node.kind == 'string':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 67:** `            return 'string'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 68:** `        if node.kind == 'boolean':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 69:** `            return 'bool'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 70:** `        if node.kind == 'variable':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 71:** `            return self.lookup(node.value)`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 72:** `        if node.kind == 'binary':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 73:** `            if node.value in ('==', '!=', '<', '>', '<=', '>='):`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 74:** `                return 'bool'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 75:** `            left = self.infer(node.children[0]); right = self.infer(node.children[1])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 76:** `            return 'float' if 'float' in (left, right) or node.value == '/' else 'int'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 77:** `        raise NativeError('No se puede inferir tipo')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 79:** `    def statement(self, node):`  
**Para qué sirve:** Define la función `statement` y sus parámetros de entrada.  

**Línea 80:** `        if node.kind == 'declare':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 81:** `            name, typ = node.value['name'], node.value['type']`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 82:** `            self.types[-1][name] = typ`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 83:** `            ctype = {'int': 'int64_t', 'float': 'double', 'bool': 'bool', 'string': 'const char *'}[typ]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 84:** `            self.write(f'{ctype} {name} = {self.expression(node.children[0])};')`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 85:** `        elif node.kind == 'assign':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 86:** `            self.write(f'{node.value} = {self.expression(node.children[0])};')`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 87:** `        elif node.kind == 'print':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 88:** `            expr = node.children[0]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 89:** `            typ = self.infer(expr)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 90:** `            fmt = {'int': '%" PRId64 "', 'float': '%.15g', 'bool': '%s', 'string': '%s'}[typ]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 91:** `            value = self.expression(expr)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 92:** `            if typ == 'bool':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 93:** `                value = f'(({value}) ? "true" : "false")'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 94:** `            self.write(f'printf("{fmt}\\n", {value});')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 95:** `        elif node.kind == 'call':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 96:** `            self.write(f'{node.value}();')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 97:** `        elif node.kind == 'return':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 98:** `            raise NativeError('Las funciones con return no tienen valor de retorno en la sintaxis actual; se requiere ampliar el lenguaje')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 99:** `        elif node.kind == 'free':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 100:** `            raise NativeError('free requiere gestión segura de memoria; no se traduce todavía al backend nativo')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 101:** `        else:`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 102:** `            raise NativeError(f'Sentencia nativa no soportada: {node.kind}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 104:** `    def generate(self, ast):`  
**Para qué sirve:** Define la función `generate` y sus parámetros de entrada.  

**Línea 105:** `        self.lines = [`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 106:** `            '/* CompilaLab: C11 generado desde AST validado. */',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 107:** `            '#include <stdio.h>',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 108:** `            '#include <stdint.h>',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 109:** `            '#include <inttypes.h>',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 110:** `            '#include <stdbool.h>',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 111:** `            '#include <string.h>',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 112:** `            '',`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 113:** `        ]`  
**Para qué sirve:** Cierra una estructura o agrupación abierta previamente.  

**Línea 114:** `        functions = [n for n in ast.children if n.kind == 'function']`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 115:** `        # Las funciones usan el mismo espacio de nombres global que el programa.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 116:** `        for fn in functions:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 117:** `            self.write(f'static void {fn.value}(void);')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 118:** `        if functions:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 119:** `            self.write('')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 120:** `        for fn in functions:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 121:** `            # Una función nativa no puede leer variables locales de main.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 122:** `            # Se rechaza expresamente en lugar de producir C incorrecto.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 123:** `            global_names = {n.value['name'] for n in ast.children if n.kind == 'declare'}`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 124:** `            def walk(n):`  
**Para qué sirve:** Define la función `walk` y sus parámetros de entrada.  

**Línea 125:** `                if n.kind == 'variable' and n.value in global_names:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 126:** `                    raise NativeError(f'La función {fn.value} accede a {n.value} de main: alcance nativo aún no soportado')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 127:** `                for child in n.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 128:** `                    walk(child)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 129:** `            for stmt in fn.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 130:** `                for child in stmt.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 131:** `                    walk(child)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 132:** `            self.write(f'static void {fn.value}(void) {{')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 133:** `            self.indent = 1`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 134:** `            self.types.append({})`  
**Para qué sirve:** Añade un elemento a una lista de trabajo o resultados.  

**Línea 135:** `            for stmt in fn.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 136:** `                self.statement(stmt)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 137:** `            self.types.pop()`  
**Para qué sirve:** Retira un elemento; en una pila sigue el principio LIFO.  

**Línea 138:** `            self.indent = 0`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 139:** `            self.write('}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 140:** `        self.write('int main(void) {')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 141:** `        self.indent = 1`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 142:** `        for stmt in ast.children:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 143:** `            if stmt.kind != 'function':`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 144:** `                self.statement(stmt)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 145:** `        self.write('return 0;')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 146:** `        self.indent = 0`  
**Para qué sirve:** Actualiza el estado interno del objeto mediante un atributo.  

**Línea 147:** `        self.write('}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 148:** `        return '\n'.join(self.lines) + '\n'`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 151:** `def find_compiler():`  
**Para qué sirve:** Define la función `find_compiler` y sus parámetros de entrada.  

**Línea 152:** `    """Busca un compilador real instalado y disponible en PATH."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 153:** `    for name in ('gcc', 'clang'):`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 154:** `        found = shutil.which(name)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 155:** `        if found:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 156:** `            return found`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 157:** `    return None`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 160:** `def build_native(source, destination=None, run=True, timeout=8):`  
**Para qué sirve:** Define la función `build_native` y sus parámetros de entrada.  

**Línea 161:** `    """Compila código CompilaLab a ejecutable nativo; devuelve C, binario y salida.`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 163:** `    El código fuente se valida primero con el frontend del proyecto. Nunca`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 164:** `    se pasa el texto original del usuario como código C sin analizar.`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 165:** `    """`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 166:** `    from compiler import lex, Parser, Semantic`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 167:** `    compiler = find_compiler()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 168:** `    if not compiler:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 169:** `        raise NativeError('No se encontró GCC ni Clang en PATH. Instala MinGW-w64 o LLVM para compilar de forma nativa.')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 170:** `    tree = Parser(lex(source)).parse()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 171:** `    Semantic().check(tree)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 172:** `    generated = CEmitter().generate(tree)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 173:** `    if destination is None:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 174:** `        folder = Path(tempfile.mkdtemp(prefix='compilalab_native_'))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 175:** `        destination = folder / ('programa.exe' if os.name == 'nt' else 'programa')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 176:** `    else:`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 177:** `        destination = Path(destination).resolve()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 178:** `        destination.parent.mkdir(parents=True, exist_ok=True)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 179:** `    c_path = destination.with_suffix('.c')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 180:** `    c_path.write_text(generated, encoding='utf-8')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 181:** `    cmd = [compiler, '-std=c11', '-O0', '-Wall', '-Wextra', str(c_path), '-o', str(destination)]`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 182:** `    try:`  
**Para qué sirve:** Inicia un bloque que puede producir excepciones controladas.  

**Línea 183:** `        build = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 184:** `    except subprocess.TimeoutExpired as error:`  
**Para qué sirve:** Captura un error y permite manejarlo sin terminar abruptamente.  

**Línea 185:** `        raise NativeError('El compilador nativo superó el tiempo límite') from error`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 186:** `    if build.returncode:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 187:** `        raise NativeError('Error del compilador C:\n' + build.stderr[-4000:])`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 188:** `    output = None`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 189:** `    if run:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 190:** `        try:`  
**Para qué sirve:** Inicia un bloque que puede producir excepciones controladas.  

**Línea 191:** `            executed = subprocess.run([str(destination)], capture_output=True, text=True, timeout=timeout, check=False)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 192:** `        except subprocess.TimeoutExpired as error:`  
**Para qué sirve:** Captura un error y permite manejarlo sin terminar abruptamente.  

**Línea 193:** `            raise NativeError('El ejecutable nativo superó el tiempo límite') from error`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 194:** `        if executed.returncode:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 195:** `            raise NativeError(f'El programa nativo terminó con código {executed.returncode}: {executed.stderr[-2000:]}')`  
**Para qué sirve:** Lanza una excepción para indicar una condición inválida.  

**Línea 196:** `        output = executed.stdout`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 197:** `    return {'c_source': generated, 'c_path': str(c_path), 'executable': str(destination),`  
**Para qué sirve:** Devuelve el resultado de la función al código que la llamó.  

**Línea 198:** `            'compiler': compiler, 'build_warnings': build.stderr, 'output': output}`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

## `gui.py`

**Línea 1:** `"""Interfaz local Tkinter, sin dependencias externas."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 2:** `import json`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 3:** `import tkinter as tk`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 4:** `from tkinter import ttk, filedialog`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 5:** `from pathlib import Path`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 6:** `from compiler import compile_source`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 7:** `from coverage import COVERAGE`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 8:** `from native_backend import build_native, NativeError, find_compiler`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 10:** `BASE=Path(__file__).resolve().parent`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 11:** `root=tk.Tk(); root.title('CompilaLab v10 &#124; Laboratorio integral de compiladores'); root.geometry('1420x850')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 12:** `root.configure(bg='#101b2c')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 13:** `style=ttk.Style(); style.theme_use('clam')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 14:** `style.configure('TNotebook',background='#101b2c'); style.configure('TNotebook.Tab',padding=(15,9))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 15:** `header=tk.Frame(root,bg='#101b2c'); header.pack(fill='x',padx=20,pady=(14,8))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 16:** `tk.Label(header,text='CompilaLab',font=('Segoe UI',24,'bold'),fg='#e9f4ff',bg='#101b2c').pack(side='left')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 17:** `tk.Label(header,text='  Lexer → AST → Semántica → TAC → CPU / RAM',font=('Segoe UI',11),fg='#92a6bf',bg='#101b2c').pack(side='left',padx=14)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 18:** `bar=tk.Frame(root,bg='#101b2c'); bar.pack(fill='x',padx=20,pady=7)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 19:** `reg=tk.IntVar(value=3); optimize=tk.BooleanVar(value=False)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 20:** `tk.Label(bar,text='Registros:',bg='#101b2c',fg='white').pack(side='left')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 21:** `ttk.Spinbox(bar,from_=3,to=16,textvariable=reg,width=4).pack(side='left',padx=6)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 22:** `ttk.Checkbutton(bar,text='Activar optimización',variable=optimize).pack(side='left',padx=15)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 23:** `status=tk.StringVar(value='Preparado para compilar')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 24:** `main=tk.PanedWindow(root,orient='horizontal',sashwidth=7,bg='#101b2c'); main.pack(fill='both',expand=True,padx=20,pady=8)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 25:** `left=tk.Frame(main,bg='#17263a'); right=tk.Frame(main,bg='#17263a'); main.add(left,minsize=350,width=450); main.add(right,minsize=500)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 26:** `tk.Label(left,text='CÓDIGO FUENTE',font=('Segoe UI',11,'bold'),bg='#17263a',fg='white').pack(anchor='w',padx=12,pady=10)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 27:** `editor=tk.Text(left,font=('Consolas',12),bg='#0e1828',fg='#dceeff',insertbackground='white',undo=True,wrap='none',padx=12,pady=12)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 28:** `editor.pack(fill='both',expand=True,padx=12,pady=(0,12)); editor.insert('1.0',(BASE/'examples'/'correcto.clab').read_text(encoding='utf-8'))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 29:** `notebook=ttk.Notebook(right); notebook.pack(fill='both',expand=True,padx=12,pady=12)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 30:** `views={}`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 31:** `for name in ['Tokens','Autómatas','Gramática','AST','Símbolos','TAC','Optimización','Ensamblador','Spill','Memoria','CPU virtual','Paso a paso','Cobertura','Salida','C nativo','Salida nativa']:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 32:** `    frame=tk.Frame(notebook,bg='#0e1828'); notebook.add(frame,text=name)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 33:** `    widget=tk.Text(frame,font=('Consolas',11),bg='#0e1828',fg='#dceeff',insertbackground='white',wrap='none',padx=14,pady=14)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 34:** `    widget.pack(fill='both',expand=True); views[name]=widget`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 36:** `last_result={}`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 37:** `step_index=tk.IntVar(value=0)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 39:** `def show_step():`  
**Para qué sirve:** Define la función `show_step` y sus parámetros de entrada.  

**Línea 40:** `    trace=last_result.get('cpu_trace',[])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 41:** `    if not trace:`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 42:** `        message='Sin traza. Compila un programa válido.'`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 43:** `    else:`  
**Para qué sirve:** Ejecuta la alternativa cuando no se cumple la condición anterior.  

**Línea 44:** `        index=max(0,min(step_index.get(),len(trace)-1)); step_index.set(index)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 45:** `        message=json.dumps({'paso':index+1,'total':len(trace),**trace[index]},ensure_ascii=False,indent=2)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 46:** `    w=views['Paso a paso']; w.delete('1.0','end'); w.insert('1.0',message)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 48:** `def advance_step(delta):`  
**Para qué sirve:** Define la función `advance_step` y sus parámetros de entrada.  

**Línea 49:** `    step_index.set(step_index.get()+delta); show_step(); notebook.select(list(views).index('Paso a paso'))`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 51:** `def compile_action():`  
**Para qué sirve:** Define la función `compile_action` y sus parámetros de entrada.  

**Línea 52:** `    r=compile_source(editor.get('1.0','end-1c'),reg.get(),optimize.get())`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 53:** `    last_result.clear(); last_result.update(r); step_index.set(0)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 54:** `    data={'Tokens':r.get('tokens',[]),'Autómatas':r.get('automata',[]),'Gramática':r.get('grammar',''),'AST':r.get('ast',{}),'Símbolos':r.get('symbols',[]),'TAC':r.get('tac',[]),'Optimización':{'notas':r.get('optimizations',[]),'tac':r.get('optimized_tac',[])},'Ensamblador':r.get('assembly',[]),'Spill':{'cantidad':r.get('spill_count',0),'eventos':r.get('register_events',[]),'slots':r.get('register_slots',{})},'Memoria':{'eventos':r.get('memory_events',[]),'variables':r.get('globals',{}),'heap_pendiente':r.get('heap_remaining',{})},'CPU virtual':{'salida_cpu':r.get('cpu_output',[]),'coincide_con_tac':r.get('cpu_matches_tac'),'registros_finales':r.get('cpu_registers',{}),'ram_spill':r.get('cpu_ram',{}),'heap_final':r.get('cpu_heap_remaining',{}),'eventos_memoria':r.get('cpu_memory_events',[]),'traza':r.get('cpu_trace',[])},'Paso a paso':{},'Cobertura':[{'semana':week,'concepto':concept,'ubicacion':location,'estado':status} for week,concept,location,status in COVERAGE],'Salida':r.get('output',[])}`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 55:** `    for key,value in data.items():`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 56:** `        w=views[key]; w.delete('1.0','end'); w.insert('1.0','\n'.join(map(str,value)) if isinstance(value,list) and key not in ('Tokens','Símbolos') else json.dumps(value,ensure_ascii=False,indent=2))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 57:** `    show_step()`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 58:** `    status.set(('✓ Compilación exitosa · Spill: '+str(r.get('spill_count',0))) if r['success'] else '✗ '+r['error'])`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 59:** `    notebook.select(list(views).index('Salida') if r['success'] else 0)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 61:** `def native_action():`  
**Para qué sirve:** Define la función `native_action` y sus parámetros de entrada.  

**Línea 62:** `    # Traduce el programa al AST, genera C11, invoca GCC/Clang y ejecuta el binario real.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 63:** `    try:`  
**Para qué sirve:** Inicia un bloque que puede producir excepciones controladas.  

**Línea 64:** `        result = build_native(editor.get('1.0', 'end-1c'))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 65:** `        for tab, value in [('C nativo', result['c_source']), ('Salida nativa', result['output'])]:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 66:** `            views[tab].delete('1.0', 'end')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 67:** `            views[tab].insert('1.0', value)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 68:** `        status.set('✓ Compilación NATIVA exitosa: ' + result['executable'])`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 69:** `        notebook.select(list(views).index('Salida nativa'))`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 70:** `    except Exception as error:`  
**Para qué sirve:** Captura un error y permite manejarlo sin terminar abruptamente.  

**Línea 71:** `        # La interfaz informa el error y permanece abierta.`  
**Para qué sirve:** Comentario original del desarrollador que explica el contexto.  

**Línea 72:** `        views['Salida nativa'].delete('1.0', 'end')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 73:** `        views['Salida nativa'].insert('1.0', str(error))`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 74:** `        status.set('✗ Compilación nativa fallida: ' + str(error)[:110])`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 75:** `        notebook.select(list(views).index('Salida nativa'))`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 77:** `def open_action():`  
**Para qué sirve:** Define la función `open_action` y sus parámetros de entrada.  

**Línea 78:** `    file=filedialog.askopenfilename(filetypes=[('CompilaLab','*.clab'),('Todos','*.*')])`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 79:** `    if file: editor.delete('1.0','end'); editor.insert('1.0',Path(file).read_text(encoding='utf-8'))`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 81:** `def example(name):`  
**Para qué sirve:** Define la función `example` y sus parámetros de entrada.  

**Línea 82:** `    editor.delete('1.0','end'); editor.insert('1.0',(BASE/'examples'/name).read_text(encoding='utf-8')); compile_action()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 84:** `ttk.Button(bar,text='▶ Compilar y ejecutar',command=compile_action).pack(side='left',padx=8)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 85:** `ttk.Button(bar,text='▶ Ejecutable REAL (GCC/Clang)',command=native_action).pack(side='left',padx=5)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 86:** `ttk.Button(bar,text='Abrir archivo',command=open_action).pack(side='left',padx=8)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 87:** `for label,name in [('Correcto','correcto.clab'),('Spill','spill.clab'),('Tipos','tipos_error.clab'),('Stack / Heap','memoria.clab'),('Optimiz.','optimizacion.clab')]:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 88:** `    ttk.Button(bar,text=label,command=lambda n=name:example(n)).pack(side='left',padx=3)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 89:** `ttk.Button(bar,text='◀ CPU',command=lambda:advance_step(-1)).pack(side='left',padx=3)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 90:** `ttk.Button(bar,text='CPU ▶',command=lambda:advance_step(1)).pack(side='left',padx=3)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 91:** `tk.Label(root,textvariable=status,anchor='w',font=('Segoe UI',11),bg='#101b2c',fg='#86d8c5').pack(fill='x',padx=20,pady=(0,12))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 92:** `compile_action(); root.mainloop()`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

## `coverage.py`

**Línea 1:** `"""Mapa de teoría y código: trazabilidad pedagógica, no certificación industrial."""`  
**Para qué sirve:** Inicio, continuación o cierre de documentación interna (docstring).  

**Línea 2:** `COVERAGE = [`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 3:** ` ('1-2','Arquitectura del compilador','compiler.compile_source','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 4:** ` ('1-2','Tokens, lexemas, regex, errores léxicos','compiler.lex','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 5:** ` ('1-2','AFD de identificadores y números','automata.identifier_dfa / number_dfa','Demostración didáctica'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 6:** ` ('1-2','AFN, conversión AFN a AFD, minimización','docs/TEORIA_Y_LIMITACIONES.md','Solo teoría'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 7:** ` ('3-4','Gramática y precedencia','automata.GRAMMAR / compiler.Parser','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 8:** ` ('3-4','Descenso recursivo Top-Down y AST','compiler.Parser / Node','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 9:** ` ('3-4','Bottom-Up LR/LALR','docs/TEORIA_Y_LIMITACIONES.md','Solo teoría'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 10:** ` ('5','Tabla de símbolos, ámbitos de función','compiler.Semantic','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 11:** ` ('5','Ámbitos anidados arbitrarios y shadowing','docs/TEORIA_Y_LIMITACIONES.md','Parcial'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 12:** ` ('6','Tipos, conversiones permitidas y errores','compiler.Semantic.expr','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 13:** ` ('7','IR, TAC y cuádruplas','compiler.IRBuilder / Quad','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 14:** ` ('8','Stack LIFO, Stack Frames y Heap','compiler.Memory','Simulación'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 15:** ` ('9','Propagación y plegado de constantes','compiler.optimize','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 16:** ` ('9','Eliminación de temporales muertos','compiler.eliminate_dead_temporaries','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 17:** ` ('9','Optimización global y flujo de control','docs/TEORIA_Y_LIMITACIONES.md','Solo teoría'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 18:** ` ('10','Selección de instrucciones, ensamblador','compiler.Backend','Implementado (ISA virtual)'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 19:** ` ('10','Registros, liveness aproximado y Spill','compiler.Backend','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 20:** ` ('10','Coloreado de grafos','docs/TEORIA_Y_LIMITACIONES.md','Solo teoría'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 21:** ` ('10','CPU virtual y RAM de Spill','virtual_cpu.VirtualCPU','Simulación'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 22:** ` ('10','Pruebas del pipeline y errores','tests/','Implementado'),`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 23:** `]`  
**Para qué sirve:** Cierra una estructura o agrupación abierta previamente.  

## `main.py`

**Línea 1:** `import argparse`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 2:** `import json`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 3:** `from pathlib import Path`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 4:** `from compiler import compile_source`  
**Para qué sirve:** Importa clases, funciones o módulos que necesita este archivo.  

**Línea 6:** `BASE=Path(__file__).resolve().parent`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 8:** `def main():`  
**Para qué sirve:** Define la función `main` y sus parámetros de entrada.  

**Línea 9:** `    p=argparse.ArgumentParser(description='CompilaLab — compilador educativo')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 10:** `    p.add_argument('file',nargs='?',default=str(BASE/'examples'/'correcto.clab'))`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 11:** `    p.add_argument('--registers',type=int,default=3)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 12:** `    p.add_argument('--optimize',action='store_true')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 13:** `    p.add_argument('--json',action='store_true')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 14:** `    a=p.parse_args()`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 15:** `    if a.registers<3: p.error('Se requieren al menos 3 registros para esta ISA virtual')`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 16:** `    source=Path(a.file).read_text(encoding='utf-8')`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 17:** `    r=compile_source(source,a.registers,a.optimize)`  
**Para qué sirve:** Asigna o actualiza un valor que utilizará el algoritmo.  

**Línea 18:** `    if a.json: print(json.dumps(r,indent=2,ensure_ascii=False)); return`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 19:** `    print('=== CÓDIGO FUENTE ===\n'+source)`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 20:** `    for key,title in [('tokens','TOKENS'),('ast','AST'),('symbols','TABLA DE SÍMBOLOS'),('tac','TAC'),('optimized_tac','TAC OPTIMIZADO'),('optimizations','OPTIMIZACIONES'),('assembly','ENSAMBLADOR VIRTUAL'),('register_events','REGISTROS Y SPILL'),('memory_events','MEMORIA STACK/HEAP'),('output','SALIDA')]:`  
**Para qué sirve:** Itera sobre una secuencia o colección de elementos.  

**Línea 21:** `        if key in r: print(f'\n=== {title} ===\n'+(json.dumps(r[key],indent=2,ensure_ascii=False) if key in ('tokens','ast','symbols') else '\n'.join(map(str,r[key]))))`  
**Para qué sirve:** Evalúa una condición para decidir qué rama del algoritmo ejecutar.  

**Línea 22:** `    print(f'\nSPILLS: {r.get("spill_count",0)}')`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 23:** `    print('OK' if r['success'] else 'ERROR: '+r['error'])`  
**Para qué sirve:** Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.  

**Línea 25:** `if __name__=='__main__': main()`  
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
