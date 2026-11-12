"""Backend nativo: traduce el AST validado a C11 y lo compila con GCC o Clang.

El resultado es un ejecutable de máquina REAL, no una CPU simulada.
La selección de registros físicos corresponde al compilador C instalado.
"""
from __future__ import annotations
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from dataclasses import dataclass


class NativeError(Exception):
    """Error de traducción, compilación o ejecución nativa."""


def c_string(value):
    """Escapa una cadena para convertirla en un literal C válido."""
    import json
    return json.dumps(value, ensure_ascii=True)


class CEmitter:
    """Genera C11 desde el AST de CompilaLab, respetando sus tipos y ámbitos."""
    def __init__(self):
        self.types = [{}]
        self.indent = 0
        self.lines = []

    def write(self, statement):
        self.lines.append('    ' * self.indent + statement)

    def lookup(self, name):
        for scope in reversed(self.types):
            if name in scope:
                return scope[name]
        raise NativeError(f'Variable no declarada: {name}')

    def expression(self, node):
        if node.kind == 'number':
            return node.value
        if node.kind == 'string':
            return c_string(node.value)
        if node.kind == 'boolean':
            return 'true' if node.value else 'false'
        if node.kind == 'variable':
            return node.value
        if node.kind == 'binary':
            left, right = node.children
            if node.value == '/':
                # CompilaLab define división real incluso para dos enteros.
                return f'((double)({self.expression(left)}) / (double)({self.expression(right)}))'
            if self.infer(left) == 'string' and self.infer(right) == 'string' and node.value in ('==', '!='):
                test = '== 0' if node.value == '==' else '!= 0'
                return f'(strcmp({self.expression(left)}, {self.expression(right)}) {test})'
            return f'({self.expression(left)} {node.value} {self.expression(right)})'
        if node.kind == 'new':
            raise NativeError('new/free requieren gestión segura de memoria; no se traducen todavía al backend nativo')
        raise NativeError(f'Expresión nativa no soportada: {node.kind}')

    def infer(self, node):
        if node.kind == 'number':
            return 'float' if '.' in node.value else 'int'
        if node.kind == 'string':
            return 'string'
        if node.kind == 'boolean':
            return 'bool'
        if node.kind == 'variable':
            return self.lookup(node.value)
        if node.kind == 'binary':
            if node.value in ('==', '!=', '<', '>', '<=', '>='):
                return 'bool'
            left = self.infer(node.children[0]); right = self.infer(node.children[1])
            return 'float' if 'float' in (left, right) or node.value == '/' else 'int'
        raise NativeError('No se puede inferir tipo')

    def statement(self, node):
        if node.kind == 'declare':
            name, typ = node.value['name'], node.value['type']
            self.types[-1][name] = typ
            ctype = {'int': 'int64_t', 'float': 'double', 'bool': 'bool', 'string': 'const char *'}[typ]
            self.write(f'{ctype} {name} = {self.expression(node.children[0])};')
        elif node.kind == 'assign':
            self.write(f'{node.value} = {self.expression(node.children[0])};')
        elif node.kind == 'print':
            expr = node.children[0]
            typ = self.infer(expr)
            fmt = {'int': '%" PRId64 "', 'float': '%.15g', 'bool': '%s', 'string': '%s'}[typ]
            value = self.expression(expr)
            if typ == 'bool':
                value = f'(({value}) ? "true" : "false")'
            self.write(f'printf("{fmt}\\n", {value});')
        elif node.kind == 'call':
            self.write(f'{node.value}();')
        elif node.kind == 'return':
            raise NativeError('Las funciones con return no tienen valor de retorno en la sintaxis actual; se requiere ampliar el lenguaje')
        elif node.kind == 'free':
            raise NativeError('free requiere gestión segura de memoria; no se traduce todavía al backend nativo')
        else:
            raise NativeError(f'Sentencia nativa no soportada: {node.kind}')

    def generate(self, ast):
        self.lines = [
            '/* CompilaLab: C11 generado desde AST validado. */',
            '#include <stdio.h>',
            '#include <stdint.h>',
            '#include <inttypes.h>',
            '#include <stdbool.h>',
            '#include <string.h>',
            '',
        ]
        functions = [n for n in ast.children if n.kind == 'function']
        # Las funciones usan el mismo espacio de nombres global que el programa.
        for fn in functions:
            self.write(f'static void {fn.value}(void);')
        if functions:
            self.write('')
        for fn in functions:
            # Una función nativa no puede leer variables locales de main.
            # Se rechaza expresamente en lugar de producir C incorrecto.
            global_names = {n.value['name'] for n in ast.children if n.kind == 'declare'}
            def walk(n):
                if n.kind == 'variable' and n.value in global_names:
                    raise NativeError(f'La función {fn.value} accede a {n.value} de main: alcance nativo aún no soportado')
                for child in n.children:
                    walk(child)
            for stmt in fn.children:
                for child in stmt.children:
                    walk(child)
            self.write(f'static void {fn.value}(void) {{')
            self.indent = 1
            self.types.append({})
            for stmt in fn.children:
                self.statement(stmt)
            self.types.pop()
            self.indent = 0
            self.write('}')
        self.write('int main(void) {')
        self.indent = 1
        for stmt in ast.children:
            if stmt.kind != 'function':
                self.statement(stmt)
        self.write('return 0;')
        self.indent = 0
        self.write('}')
        return '\n'.join(self.lines) + '\n'


def find_compiler():
    """Busca un compilador real instalado y disponible en PATH."""
    for name in ('gcc', 'clang'):
        found = shutil.which(name)
        if found:
            return found
    return None


def build_native(source, destination=None, run=True, timeout=8):
    """Compila código CompilaLab a ejecutable nativo; devuelve C, binario y salida.

    El código fuente se valida primero con el frontend del proyecto. Nunca
    se pasa el texto original del usuario como código C sin analizar.
    """
    from compiler import lex, Parser, Semantic
    compiler = find_compiler()
    if not compiler:
        raise NativeError('No se encontró GCC ni Clang en PATH. Instala MinGW-w64 o LLVM para compilar de forma nativa.')
    tree = Parser(lex(source)).parse()
    Semantic().check(tree)
    generated = CEmitter().generate(tree)
    if destination is None:
        folder = Path(tempfile.mkdtemp(prefix='compilalab_native_'))
        destination = folder / ('programa.exe' if os.name == 'nt' else 'programa')
    else:
        destination = Path(destination).resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
    c_path = destination.with_suffix('.c')
    c_path.write_text(generated, encoding='utf-8')
    cmd = [compiler, '-std=c11', '-O0', '-Wall', '-Wextra', str(c_path), '-o', str(destination)]
    try:
        build = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as error:
        raise NativeError('El compilador nativo superó el tiempo límite') from error
    if build.returncode:
        raise NativeError('Error del compilador C:\n' + build.stderr[-4000:])
    output = None
    if run:
        try:
            executed = subprocess.run([str(destination)], capture_output=True, text=True, timeout=timeout, check=False)
        except subprocess.TimeoutExpired as error:
            raise NativeError('El ejecutable nativo superó el tiempo límite') from error
        if executed.returncode:
            raise NativeError(f'El programa nativo terminó con código {executed.returncode}: {executed.stderr[-2000:]}')
        output = executed.stdout
    return {'c_source': generated, 'c_path': str(c_path), 'executable': str(destination),
            'compiler': compiler, 'build_warnings': build.stderr, 'output': output}
