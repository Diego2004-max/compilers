"""CompilaLab: compilador educativo para una CPU virtual de 3 registros."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from collections import Counter
import re

@dataclass
class Token:
    kind: str
    value: str
    line: int
    column: int

class CompileError(Exception):
    def __init__(self, phase, line, column, message):
        super().__init__(f'{phase} (línea {line}, columna {column}): {message}')
        self.phase, self.line, self.column, self.message = phase, line, column, message

PATTERN = re.compile(r'(?P<COMMENT>//[^\n]*)|(?P<SPACE>[ \t\r]+)|(?P<NEWLINE>\n)|(?P<NUMBER>\d+(?:\.\d+)?)|(?P<STRING>"(?:[^"\\]|\\.)*")|(?P<ID>[a-zA-Z_][\w]*)|(?P<OP>==|!=|<=|>=|[+*/=;(){}<>,-])|(?P<INVALID>.)')
KEYWORDS = {'int','float','string','bool','true','false','print','fn','return','new','free'}

def lex(source):
    tokens=[]; line=1; col=1
    for m in PATTERN.finditer(source):
        kind=m.lastgroup; val=m.group()
        if kind=='NEWLINE': line+=1; col=1; continue
        if kind in ('SPACE','COMMENT'): col+=len(val); continue
        if kind=='STRING' and '\n' in val: raise CompileError('Léxico',line,col,'Cadena sin cerrar')
        if kind=='INVALID': raise CompileError('Léxico',line,col,f'Carácter inválido {val!r}')
        if kind=='ID' and val in KEYWORDS: kind=val.upper()
        if kind=='OP': kind=val
        tokens.append(Token(kind,val,line,col)); col+=len(val)
    tokens.append(Token('EOF','',line,col))
    return tokens

@dataclass
class Node:
    kind: str
    line: int
    value: object=None
    children: tuple=()
    def json(self):
        return {'kind':self.kind,'line':self.line,'value':self.value,'children':[c.json() for c in self.children]}

class Parser:
    def __init__(self,tokens): self.ts=tokens; self.i=0
    def at(self,*kinds): return self.ts[self.i].kind in kinds
    def take(self,kind=None):
        t=self.ts[self.i]
        if kind and t.kind!=kind: raise CompileError('Sintáctico',t.line,t.column,f'Se esperaba {kind}, llegó {t.value or "fin de archivo"!r}')
        self.i+=1; return t
    def parse(self):
        items=[]
        while not self.at('EOF'): items.append(self.statement())
        return Node('program',1,children=tuple(items))
    def statement(self):
        t=self.ts[self.i]
        if self.at('INT','FLOAT','STRING','BOOL'):
            typ=self.take().value; name=self.take('ID'); self.take('='); exp=self.expr(); self.take(';')
            return Node('declare',t.line,{'type':typ,'name':name.value},(exp,))
        if self.at('PRINT'):
            self.take(); self.take('('); exp=self.expr(); self.take(')'); self.take(';')
            return Node('print',t.line,children=(exp,))
        if self.at('FREE'):
            self.take(); self.take('('); name=self.take('ID'); self.take(')'); self.take(';')
            return Node('free',t.line,name.value)
        if self.at('FN'):
            self.take(); name=self.take('ID'); self.take('('); self.take(')'); self.take('{')
            body=[]
            while not self.at('}','EOF'): body.append(self.statement())
            self.take('}')
            return Node('function',t.line,name.value,tuple(body))
        if self.at('RETURN'):
            self.take(); exp=self.expr(); self.take(';'); return Node('return',t.line,children=(exp,))
        if self.at('ID'):
            name=self.take();
            if self.at('('):
                self.take('('); self.take(')'); self.take(';'); return Node('call',t.line,name.value)
            self.take('='); exp=self.expr(); self.take(';'); return Node('assign',t.line,name.value,(exp,))
        raise CompileError('Sintáctico',t.line,t.column,f'Sentencia inesperada {t.value!r}')
    def expr(self): return self.comparison()
    def comparison(self):
        left=self.add()
        while self.at('==','!=','<','>','<=','>='):
            op=self.take(); left=Node('binary',op.line,op.value,(left,self.add()))
        return left
    def add(self):
        left=self.mul()
        while self.at('+','-'):
            op=self.take(); left=Node('binary',op.line,op.value,(left,self.mul()))
        return left
    def mul(self):
        left=self.unary()
        while self.at('*','/'):
            op=self.take(); left=Node('binary',op.line,op.value,(left,self.unary()))
        return left
    def unary(self):
        if self.at('-'):
            t=self.take(); return Node('binary',t.line,'-', (Node('number',t.line,'0'),self.unary()))
        return self.atom()
    def atom(self):
        t=self.ts[self.i]
        if self.at('NUMBER'): self.take(); return Node('number',t.line,t.value)
        if self.at('STRING'): self.take(); return Node('string',t.line,t.value[1:-1])
        if self.at('TRUE','FALSE'): self.take(); return Node('boolean',t.line,t.value=='true')
        if self.at('ID'): self.take(); return Node('variable',t.line,t.value)
        if self.at('NEW'):
            self.take(); self.take('('); size=self.take('NUMBER'); self.take(')')
            if '.' in size.value or int(size.value)<=0: raise CompileError('Sintáctico',t.line,t.column,'new requiere un entero positivo')
            return Node('new',t.line,int(size.value))
        if self.at('('): self.take(); exp=self.expr(); self.take(')'); return exp
        raise CompileError('Sintáctico',t.line,t.column,f'Expresión inesperada {t.value!r}')

class Semantic:
    def __init__(self): self.scopes=[{}]; self.symbols=[]; self.functions={}
    def lookup(self,name,line):
        for scope in reversed(self.scopes):
            if name in scope: return scope[name]
        raise CompileError('Semántico',line,1,f'Variable {name!r} no declarada')
    def expr(self,n):
        if n.kind=='number': return 'float' if '.' in n.value else 'int'
        if n.kind=='string': return 'string'
        if n.kind=='boolean': return 'bool'
        if n.kind=='new': return 'ptr'
        if n.kind=='variable': return self.lookup(n.value,n.line)
        if n.kind=='binary':
            a,b=(self.expr(c) for c in n.children)
            if n.value in ('==','!=','<','>','<=','>='):
                if a!=b and not ({a,b}<={'int','float'}): raise CompileError('Semántico',n.line,1,'Comparación de tipos incompatibles')
                return 'bool'
            if a not in ('int','float') or b not in ('int','float'):
                raise CompileError('Semántico',n.line,1,f'Operación {n.value} inválida entre {a} y {b}')
            return 'float' if 'float' in (a,b) or n.value=='/' else 'int'
        raise ValueError(n.kind)
    def check(self,root):
        for stmt in root.children:
            if stmt.kind=='function':
                if stmt.value in self.functions: raise CompileError('Semántico',stmt.line,1,'Función duplicada')
                self.functions[stmt.value]=stmt
        for stmt in root.children:
            if stmt.kind=='function':
                self.scopes.append({}); self.block(stmt.children,stmt.value); self.scopes.pop()
            else: self.block((stmt,),'global')
        return self.symbols
    def block(self,statements,scope):
        for s in statements:
            if s.kind=='declare':
                name=s.value['name']; typ=s.value['type']; found=self.expr(s.children[0]); actual='int' if typ=='int' and found=='ptr' else found
                if name in self.scopes[-1]: raise CompileError('Semántico',s.line,1,f'Declaración duplicada: {name}')
                if typ!=actual and not (typ=='float' and actual=='int'):
                    raise CompileError('Semántico',s.line,1,f'{name}: se esperaba {typ}, llegó {found}')
                self.scopes[-1][name]=typ; self.symbols.append({'name':name,'type':typ,'scope':scope,'line':s.line})
            elif s.kind=='assign':
                expected=self.lookup(s.value,s.line); actual=self.expr(s.children[0]); actual='int' if expected=='int' and actual=='ptr' else actual
                if expected!=actual and not (expected=='float' and actual=='int'):
                    raise CompileError('Semántico',s.line,1,f'{s.value}: se esperaba {expected}, llegó {actual}')
            elif s.kind in ('print','return'): self.expr(s.children[0])
            elif s.kind=='free': self.lookup(s.value,s.line)
            elif s.kind=='call':
                if s.value not in self.functions: raise CompileError('Semántico',s.line,1,f'Función {s.value} no declarada')

@dataclass
class Quad:
    op: str
    a: object=None
    b: object=None
    dest: object=None
    line: int=0
    def show(self):
        if self.op=='CONST': return f'{self.dest} = {self.a!r}'
        if self.op=='MOV': return f'{self.dest} = {self.a}'
        if self.op=='BIN': return f'{self.dest} = {self.a} {self.b[0]} {self.b[1]}'
        if self.op=='PRINT': return f'print {self.a}'
        if self.op=='ALLOC': return f'{self.dest} = alloc {self.a}'
        if self.op=='FREE': return f'free {self.a}'
        if self.op=='ENTER': return f'enter {self.a}'
        if self.op=='LEAVE': return f'leave {self.a}'
        if self.op=='CALL': return f'call {self.a}'
        if self.op=='RET': return f'return {self.a}'
        return str(self)

class IRBuilder:
    def __init__(self): self.quads=[]; self.index=0
    def emit(self,*args): self.quads.append(Quad(*args))
    def tmp(self): self.index+=1; return f't{self.index}'
    def expr(self,n):
        if n.kind in ('number','string','boolean'):
            t=self.tmp(); v=float(n.value) if n.kind=='number' and '.' in n.value else int(n.value) if n.kind=='number' else n.value
            self.emit('CONST',v,None,t,n.line); return t
        if n.kind=='variable': return n.value
        if n.kind=='new':
            t=self.tmp(); self.emit('ALLOC',n.value,None,t,n.line); return t
        if n.kind=='binary':
            left=self.expr(n.children[0]); right=self.expr(n.children[1]); t=self.tmp()
            self.emit('BIN',left,(n.value,right),t,n.line); return t
        raise ValueError(n.kind)
    def statement(self,s):
        if s.kind in ('declare','assign'):
            dst=s.value['name'] if s.kind=='declare' else s.value
            src=self.expr(s.children[0]); self.emit('MOV',src,None,dst,s.line)
        elif s.kind=='print': self.emit('PRINT',self.expr(s.children[0]),None,None,s.line)
        elif s.kind=='free': self.emit('FREE',s.value,None,None,s.line)
        elif s.kind=='call': self.emit('CALL',s.value,None,None,s.line)
        elif s.kind=='return': self.emit('RET',self.expr(s.children[0]),None,None,s.line)
    def build(self,root):
        funcs={s.value:s for s in root.children if s.kind=='function'}
        self.emit('ENTER','main',None,None,1)
        for s in root.children:
            if s.kind!='function': self.statement(s)
        self.emit('LEAVE','main',None,None,root.line)
        for name,fn in funcs.items():
            self.emit('ENTER',name,None,None,fn.line)
            for s in fn.children: self.statement(s)
            self.emit('LEAVE',name,None,None,fn.line)
        return self.quads

def calculate(op,a,b):
    if op=='+': return a+b
    if op=='-': return a-b
    if op=='*': return a*b
    if op=='/':
        if b==0: raise ZeroDivisionError('División por cero')
        return a/b
    return {'==':lambda:a==b,'!=':lambda:a!=b,'<':lambda:a<b,'>':lambda:a>b,'<=':lambda:a<=b,'>=':lambda:a>=b}[op]()

def eliminate_dead_temporaries(quads):
    """DCE conservador: elimina definiciones puras de temporales tN sin usos.

    No elimina asignaciones de usuario, llamadas, prints ni operaciones de memoria.
    """
    live=set(); kept=[]; notes=[]
    for q in reversed(quads):
        if q.op in ('CONST','MOV','BIN') and isinstance(q.dest,str) and re.fullmatch(r't\d+',q.dest) and q.dest not in live:
            notes.append(f'Línea {q.line}: temporal muerto {q.dest} eliminado')
            continue
        if q.dest is not None and q.op in ('CONST','MOV','BIN','ALLOC'):
            live.discard(q.dest)
        if q.op=='BIN': live.add(q.a); live.add(q.b[1])
        elif q.op in ('MOV','PRINT','FREE','RET') and isinstance(q.a,str): live.add(q.a)
        kept.append(q)
    return list(reversed(kept)),list(reversed(notes))

def optimize(quads):
    # Propagación de constantes y plegado, sin borrar instrucciones con efectos.
    known={}; out=[]; notes=[]
    for q in quads:
        if q.op=='ENTER': known={}
        if q.op=='CONST': known[q.dest]=q.a
        elif q.op=='MOV':
            if q.a in known:
                value=known[q.a]; q=Quad('CONST',value,None,q.dest,q.line); known[q.dest]=value; notes.append(f'Línea {q.line}: propagación de constante a {q.dest}')
            else: known.pop(q.dest,None)
        elif q.op=='BIN':
            op,right=q.b
            if q.a in known and right in known:
                try:
                    v=calculate(op,known[q.a],known[right]); q=Quad('CONST',v,None,q.dest,q.line)
                    known[q.dest]=v; notes.append(f'Línea {q.line}: plegado constante en {q.dest}')
                except ZeroDivisionError: known.pop(q.dest,None)
            else: known.pop(q.dest,None)
        elif q.op in ('CALL','LEAVE'): known={}
        out.append(q)
    # En este lenguaje, DCE de temporales es seguro en programas sin llamadas:
    # las funciones pueden compartir nombres de temporales y requieren un CFG.
    if not any(q.op in ('CALL','RET') for q in out):
        out,dead_notes=eliminate_dead_temporaries(out)
        notes.extend(dead_notes)
    return out,notes

class Memory:
    def __init__(self): self.stack=[]; self.heap={}; self.next_addr=0x1000; self.events=[]
    def push(self,name): self.stack.append({'function':name,'locals':{}}); self.events.append(f'PUSH frame {name}')
    def pop(self):
        if not self.stack: raise RuntimeError('Stack underflow')
        name=self.stack.pop()['function']; self.events.append(f'POP frame {name}')
    def alloc(self,size):
        addr=self.next_addr; self.next_addr+=size; self.heap[addr]=size; self.events.append(f'HEAP ALLOC {size} bytes en {hex(addr)}'); return addr
    def free(self,addr):
        if addr not in self.heap: raise RuntimeError(f'Doble free o puntero inválido: {hex(addr)}')
        del self.heap[addr]; self.events.append(f'HEAP FREE {hex(addr)}')

class Backend:
    """Emite ensamblador para una ISA virtual; tres registros y spill explícito."""
    def __init__(self,registers=3):
        if registers < 3: raise ValueError('Se requieren al menos 3 registros para esta ISA de tres operandos')
        self.regs=[f'R{i}' for i in range(registers)]; self.owners={}; self.locations={}; self.asm=[]; self.events=[]; self.spills=0; self.slots={}; self.slot=0
    def emit(self,s): self.asm.append(s)
    def uses(self,q):
        if q.op=='BIN': return [q.a,q.b[1]]
        if q.op in ('MOV','PRINT','FREE','RET'): return [q.a]
        return []
    def future(self,quads,i):
        return Counter(x for q in quads[i+1:] for x in self.uses(q) if isinstance(x,str))
    def reg(self,name,quads,i,protect=()):
        if name in self.locations: return self.locations[name]
        free=next((r for r in self.regs if r not in self.owners),None)
        if free is None:
            counts=self.future(quads,i)
            candidates=[(counts.get(v,0),r,v) for r,v in self.owners.items() if v not in protect]
            if not candidates: raise RuntimeError('No hay registro libre para los operandos; aumente el pool')
            _,free,victim=min(candidates)
            if counts.get(victim,0):
                if victim not in self.slots: self.slots[victim]=0x2000+self.slot*8; self.slot+=1
                self.emit(f'STORE [{hex(self.slots[victim])}], {free} ; SPILL {victim}')
                self.events.append(f'SPILL {victim}: {free} → STACK[{hex(self.slots[victim])}]'); self.spills+=1
            self.locations.pop(victim,None); self.owners.pop(free)
        self.owners[free]=name; self.locations[name]=free
        if name in self.slots:
            self.emit(f'LOAD {free}, [{hex(self.slots[name])}] ; RECARGA {name}')
            self.events.append(f'RELOAD {name}: STACK → {free}')
        return free
    def release_dead(self,quads,i):
        future=self.future(quads,i)
        for reg,name in list(self.owners.items()):
            if not future.get(name,0): self.owners.pop(reg); self.locations.pop(name,None)
    def generate(self,quads):
        for i,q in enumerate(quads):
            if q.op in ('ENTER','LEAVE','CALL'):
                if q.op=='CALL':
                    future=self.future(quads,i)
                    for register,name in list(self.owners.items()):
                        if future.get(name,0):
                            if name not in self.slots:
                                self.slots[name]=0x2000+self.slot*8; self.slot+=1
                            self.emit(f'STORE [{hex(self.slots[name])}], {register} ; CONSERVAR {name} ANTES DE CALL')
                            self.events.append(f'CALL-SAVE {name}: {register} → STACK[{hex(self.slots[name])}]')
                self.emit(f'{q.op} {q.a}'); self.owners.clear(); self.locations.clear()
            elif q.op=='CONST':
                r=self.reg(q.dest,quads,i); self.emit(f'LI {r}, {q.a!r} ; {q.dest}')
            elif q.op=='MOV':
                source=self.reg(q.a,quads,i); dest=self.reg(q.dest,quads,i,protect=(q.a,))
                self.emit(f'MOV {dest}, {source} ; {q.dest}')
            elif q.op=='BIN':
                op,right=q.b; leftreg=self.reg(q.a,quads,i)
                rightreg=self.reg(right,quads,i,protect=(q.a,))
                dest=self.reg(q.dest,quads,i,protect=(q.a,right))
                self.emit(f'{ {"+":"ADD","-":"SUB","*":"MUL","/":"DIV","==":"EQ","!=":"NE","<":"LT",">":"GT","<=":"LE",">=":"GE"}[op]} {dest}, {leftreg}, {rightreg} ; {q.dest}')
            elif q.op=='PRINT':
                r=self.reg(q.a,quads,i); self.emit(f'PRINT {r}')
            elif q.op=='ALLOC':
                r=self.reg(q.dest,quads,i); self.emit(f'ALLOC {r}, {q.a}')
            elif q.op=='FREE':
                r=self.reg(q.a,quads,i); self.emit(f'FREE {r}')
            elif q.op=='RET':
                r=self.reg(q.a,quads,i); self.emit(f'RET {r}')
            self.release_dead(quads,i)
        return self.asm

class Interpreter:
    """Ejecuta TAC y simula Stack/Heap; no ejecuta ensamblador nativo."""
    def __init__(self,quads): self.qs=quads; self.memory=Memory(); self.output=[]; self.globals={}; self.locals={}; self.calls={}; self.return_value=None
    def val(self,k):
        if k in self.locals: return self.locals[k]
        if k in self.globals: return self.globals[k]
        raise RuntimeError(f'Variable temporal no inicializada: {k}')
    def execute(self):
        entries={q.a:i for i,q in enumerate(self.qs) if q.op=='ENTER'}
        self.memory.push('main'); self.locals={}; pc=entries['main']+1; steps=0
        while pc<len(self.qs):
            steps+=1
            if steps>10000: raise RuntimeError('Límite de ejecución alcanzado')
            q=self.qs[pc]; op=q.op
            if op=='CONST': self.locals[q.dest]=q.a
            elif op=='MOV':
                v=self.val(q.a); self.locals[q.dest]=v
                if len(self.memory.stack)==1: self.globals[q.dest]=v
                self.memory.stack[-1]['locals'][q.dest]=v
            elif op=='BIN': self.locals[q.dest]=calculate(q.b[0],self.val(q.a),self.val(q.b[1]))
            elif op=='PRINT': self.output.append(str(self.val(q.a)))
            elif op=='ALLOC': self.locals[q.dest]=self.memory.alloc(q.a)
            elif op=='FREE': self.memory.free(self.val(q.a))
            elif op=='CALL':
                if q.a not in entries: raise RuntimeError(f'Función no encontrada: {q.a}')
                self.calls[len(self.memory.stack)]=(pc+1,self.locals)
                self.memory.push(q.a); self.locals={}; pc=entries[q.a]+1; continue
            elif op in ('LEAVE','RET'):
                if op=='RET': self.return_value=self.val(q.a)
                self.memory.pop()
                if not self.memory.stack: break
                pc,self.locals=self.calls.pop(len(self.memory.stack)); continue
            pc+=1
        return self.output

def compile_source(source,registers=3,optimized=False,run=True):
    result={'source':source,'error':None}
    try:
        ts=lex(source); result['tokens']=[asdict(t) for t in ts]
        from automata import analyze_automata, GRAMMAR
        result['automata']=analyze_automata(ts); result['grammar']=GRAMMAR
        ast=Parser(ts).parse(); result['ast']=ast.json()
        semantic=Semantic(); result['symbols']=semantic.check(ast)
        raw=IRBuilder().build(ast); result['tac']=[q.show() for q in raw]
        opt,notes=optimize([Quad(**asdict(q)) for q in raw]); result['optimized_tac']=[q.show() for q in opt]; result['optimizations']=notes
        chosen=opt if optimized else raw
        result['quads']=[asdict(q) for q in chosen]
        backend=Backend(registers); result['assembly']=backend.generate(chosen); result['register_events']=backend.events; result['spill_count']=backend.spills
        result['register_slots']={name:hex(addr) for name,addr in backend.slots.items()}
        if run:
            vm=Interpreter(chosen); result['output']=vm.execute(); result['memory_events']=vm.memory.events; result['globals']=vm.globals; result['heap_remaining']=vm.memory.heap
            from virtual_cpu import VirtualCPU
            cpu=VirtualCPU(result['assembly'], registers); result['cpu_output']=cpu.execute()
            result['cpu_trace']=cpu.trace; result['cpu_registers']=cpu.registers
            result['cpu_ram']={hex(k):v for k,v in cpu.ram.items()}
            result['cpu_memory_events']=cpu.memory.events
            result['cpu_heap_remaining']={hex(k):v for k,v in cpu.memory.heap.items()}
            result['cpu_matches_tac']=(result['cpu_output']==result['output'])
            if not result['cpu_matches_tac']: raise RuntimeError(f'Diferencia entre TAC {result["output"]} y CPU {result["cpu_output"]}')
        result['success']=True
    except (CompileError,RuntimeError,ZeroDivisionError,TypeError,ValueError) as e:
        result['success']=False; result['error']=str(e)
    return result
