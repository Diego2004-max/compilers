"""CPU virtual: ejecuta la ISA textual generada por CompilaLab.

Los registros son un banco limitado, las direcciones de spill viven en RAM,
y ENTER/LEAVE modelan marcos de ejecución (no instrucciones x86).
"""
import ast
import re

from compiler import Memory, calculate

class VirtualCPU:
    def __init__(self, assembly, register_count=3):
        self.instructions = list(assembly)
        self.registers = {f'R{i}': None for i in range(register_count)}
        self.ram = {}
        self.memory = Memory()
        self.output = []
        self.trace = []
        self.pc = 0
        self.calls = []
        self.labels = {}
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

    def execute(self):
        if 'main' not in self.labels:
            raise RuntimeError('No existe punto de entrada main')
        self.pc = self.labels['main']
        steps = 0
        while self.pc < len(self.instructions):
            steps += 1
            if steps > 10000:
                raise RuntimeError('CPU: límite de 10000 instrucciones')
            raw = self.instructions[self.pc]
            instruction = raw.split(';', 1)[0].strip()
            if not instruction:
                self.pc += 1
                continue
            op, _, rest = instruction.partition(' ')
            args = [arg.strip() for arg in rest.split(',')] if rest else []
            before = self.pc
            jump = None
            if op == 'ENTER':
                self.memory.push(args[0])
            elif op == 'LEAVE':
                self.memory.pop()
                if not self.calls:
                    self.trace.append({'pc': before, 'instruction': instruction, 'registers': dict(self.registers), 'ram': {hex(k):v for k,v in self.ram.items()}, 'stack': [f['function'] for f in self.memory.stack], 'heap': {hex(k):v for k,v in self.memory.heap.items()}})
                    break
                jump = self.calls.pop()
            elif op == 'CALL':
                if args[0] not in self.labels:
                    raise RuntimeError(f'CPU: función no encontrada: {args[0]}')
                self.calls.append(self.pc + 1)
                jump = self.labels[args[0]]
            elif op == 'RET':
                self.memory.pop()
                if not self.calls:
                    raise RuntimeError('CPU: RET sin llamada')
                jump = self.calls.pop()
            elif op == 'LI':
                self.registers[args[0]] = ast.literal_eval(args[1])
            elif op == 'MOV':
                self.registers[args[0]] = self.register(args[1])
            elif op == 'STORE':
                match = re.fullmatch(r'\[(0x[0-9a-fA-F]+)\]', args[0])
                if not match:
                    raise RuntimeError(f'CPU: dirección inválida {args[0]}')
                self.ram[int(match.group(1), 16)] = self.register(args[1])
            elif op == 'LOAD':
                match = re.fullmatch(r'\[(0x[0-9a-fA-F]+)\]', args[1])
                if not match:
                    raise RuntimeError(f'CPU: dirección inválida {args[1]}')
                addr = int(match.group(1), 16)
                if addr not in self.ram:
                    raise RuntimeError(f'CPU: lectura de RAM no inicializada: {hex(addr)}')
                self.registers[args[0]] = self.ram[addr]
            elif op in ('ADD', 'SUB', 'MUL', 'DIV', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'):
                symbol = {'ADD': '+', 'SUB': '-', 'MUL': '*', 'DIV': '/',
                          'EQ': '==', 'NE': '!=', 'LT': '<', 'GT': '>', 'LE': '<=', 'GE': '>='}[op]
                self.registers[args[0]] = calculate(symbol, self.register(args[1]), self.register(args[2]))
            elif op == 'PRINT':
                self.output.append(str(self.register(args[0])))
            elif op == 'ALLOC':
                self.registers[args[0]] = self.memory.alloc(int(args[1]))
            elif op == 'FREE':
                self.memory.free(self.register(args[0]))
            else:
                raise RuntimeError(f'CPU: instrucción desconocida: {instruction}')
            self.trace.append({'pc': before, 'instruction': instruction, 'registers': dict(self.registers), 'ram': {hex(k):v for k,v in self.ram.items()}, 'stack': [f['function'] for f in self.memory.stack], 'heap': {hex(k):v for k,v in self.memory.heap.items()}})
            self.pc = jump if jump is not None else self.pc + 1
        return self.output
