"""CPU virtual: ejecuta la ISA textual que emite compiler.Backend.

Ciclo clásico fetch → decode → execute (como una CPU real, pero sobre texto):
    fetch   = leer self.instructions[self.pc]
    decode  = separar opcode y operandos ("ADD R2, R0, R1" → 'ADD', ['R2','R0','R1'])
    execute = actualizar registros / RAM / pila y mover el PC

Los registros son un banco LIMITADO (el mismo número que usó el Backend); la RAM
es un dict dirección → valor donde viven los spills (0x2000...). ENTER/LEAVE modelan
marcos de función, no son instrucciones x86.
(?) ¿Es ensamblador real? No: es una ISA propia. Lo que se demuestra es que el
    código objetivo es EJECUTABLE y produce lo mismo que el TAC (semántica preservada).
"""
import ast
import re

from compiler import Memory, calculate, format_value

ADDRESS = re.compile(r'\[(0x[0-9a-fA-F]+)\]')

# opcode de 3 operandos → operador de calculate(). Es la inversa de compiler.OPCODES:
# si alguien agrega un operador al Backend y olvida este mapa, la CPU lo rechaza.
ALU = {'ADD': '+', 'SUB': '-', 'MUL': '*', 'DIV': '/',
       'EQ': '==', 'NE': '!=', 'LT': '<', 'GT': '>', 'LE': '<=', 'GE': '>=',
       'AND': '&&', 'OR': '||'}


class VirtualCPU:
    def __init__(self, assembly, register_count=3):
        self.instructions = list(assembly)
        # None = registro "sin inicializar": leerlo es un bug del Backend, no un 0 silencioso.
        self.registers = {f'R{i}': None for i in range(register_count)}
        self.ram = {}
        self.memory = Memory()
        self.output = []
        self.trace = []
        self.pc = 0
        self.calls = []          # pila de direcciones de retorno (lo que en x86 empuja CALL)
        self.labels = {}
        # Pre-pasada: resolver etiquetas ANTES de ejecutar (como lo hace un ensamblador
        # de dos pasadas), para poder saltar a funciones definidas más abajo.
        for index, raw in enumerate(self.instructions):
            instruction = raw.split(';', 1)[0].strip()
            if instruction.startswith('ENTER '):
                self.labels[instruction.split()[1]] = index

    def register(self, name):
        if name not in self.registers:
            raise RuntimeError(f'Registro desconocido: {name}')
        value = self.registers[name]
        if value is None:
            raise RuntimeError(f'Lectura de registro no inicializado: {name} (PC={self.pc})')
        return value

    def address(self, operand):
        match = ADDRESS.fullmatch(operand)
        if not match:
            raise RuntimeError(f'CPU: dirección inválida {operand}')
        return int(match.group(1), 16)

    def snapshot(self, pc, instruction):
        """Foto del estado DESPUÉS de ejecutar `instruction`: alimenta la pestaña Paso a paso."""
        self.trace.append({'pc': pc, 'instruction': instruction,
                           'registers': dict(self.registers),
                           'ram': {hex(k): v for k, v in self.ram.items()},
                           'stack': [f['function'] for f in self.memory.stack],
                           'heap': {hex(k): v for k, v in self.memory.heap.items()}})

    def execute(self):
        if 'main' not in self.labels:
            raise RuntimeError('No existe punto de entrada main')
        self.pc = self.labels['main']
        steps = 0
        while self.pc < len(self.instructions):
            steps += 1
            if steps > 10000:
                raise RuntimeError('CPU: límite de 10000 instrucciones')
            # ── fetch ──
            raw = self.instructions[self.pc]
            instruction = raw.split(';', 1)[0].strip()      # lo que va tras ';' es comentario del Backend
            if not instruction:
                self.pc += 1
                continue
            # ── decode ──
            op, _, rest = instruction.partition(' ')
            args = [arg.strip() for arg in rest.split(',')] if rest else []
            before = self.pc
            jump = None
            # ── execute ──
            if op == 'ENTER':
                self.memory.push(args[0])
            elif op == 'LEAVE':
                self.memory.pop()
                if not self.calls:                 # LEAVE de main: fin del programa
                    self.snapshot(before, instruction)
                    break
                jump = self.calls.pop()
            elif op == 'CALL':
                if args[0] not in self.labels:
                    raise RuntimeError(f'CPU: función no encontrada: {args[0]}')
                self.calls.append(self.pc + 1)     # dirección de retorno = instrucción siguiente
                jump = self.labels[args[0]]
            elif op == 'RET':
                self.memory.pop()
                if not self.calls:
                    raise RuntimeError('CPU: RET sin llamada')
                jump = self.calls.pop()
            elif op == 'LI':
                self.registers[args[0]] = ast.literal_eval(args[1])   # literal seguro: nunca eval()
            elif op == 'MOV':
                self.registers[args[0]] = self.register(args[1])
            elif op == 'STORE':                    # registro → RAM   (mitad "salida" de un spill)
                self.ram[self.address(args[0])] = self.register(args[1])
            elif op == 'LOAD':                     # RAM → registro   (mitad "regreso" de un spill)
                addr = self.address(args[1])
                if addr not in self.ram:
                    raise RuntimeError(f'CPU: lectura de RAM no inicializada: {hex(addr)}')
                self.registers[args[0]] = self.ram[addr]
            elif op in ALU:
                self.registers[args[0]] = calculate(ALU[op], self.register(args[1]), self.register(args[2]))
            elif op == 'PRINT':
                self.output.append(format_value(self.register(args[0])))
            elif op == 'ALLOC':
                self.registers[args[0]] = self.memory.alloc(int(args[1]))
            elif op == 'FREE':
                self.memory.free(self.register(args[0]))
            else:
                raise RuntimeError(f'CPU: instrucción desconocida: {instruction}')
            self.snapshot(before, instruction)
            self.pc = jump if jump is not None else self.pc + 1
        return self.output
