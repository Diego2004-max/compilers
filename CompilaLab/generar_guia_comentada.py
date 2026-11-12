"""Genera un manual explicando cada línea no vacía del código del proyecto.

Se escribe en Markdown para no insertar comentarios dentro de cadenas multilínea,
lo que podría romper el programa. Se mantiene el número de línea original.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'docs' / 'CODIGO_LINEA_POR_LINEA.md'
FILES = ['compiler.py', 'automata.py', 'virtual_cpu.py', 'native_backend.py',
         'gui.py', 'coverage.py', 'main.py', 'generar_guia_comentada.py']


def explain(line):
    s = line.strip()
    if s.startswith('#'):
        return 'Comentario original del desarrollador que explica el contexto.'
    if s.startswith('"""') or s.startswith("'''"):
        return 'Inicio, continuación o cierre de documentación interna (docstring).'
    if s.startswith('from ') or s.startswith('import '):
        return 'Importa clases, funciones o módulos que necesita este archivo.'
    if s.startswith('@dataclass'):
        return 'Genera automáticamente métodos para una clase de datos.'
    if s.startswith('@'):
        return 'Decorador que modifica o configura la definición siguiente.'
    if s.startswith('class '):
        return 'Declara una clase y define la responsabilidad de sus objetos.'
    if s.startswith('def '):
        name = s.split('def ', 1)[1].split('(', 1)[0]
        return f'Define la función `{name}` y sus parámetros de entrada.'
    if s.startswith('if ') or s.startswith('elif '):
        return 'Evalúa una condición para decidir qué rama del algoritmo ejecutar.'
    if s.startswith('else:'):
        return 'Ejecuta la alternativa cuando no se cumple la condición anterior.'
    if s.startswith('for '):
        return 'Itera sobre una secuencia o colección de elementos.'
    if s.startswith('while '):
        return 'Repite un bloque mientras la condición siga siendo verdadera.'
    if s.startswith('try:'):
        return 'Inicia un bloque que puede producir excepciones controladas.'
    if s.startswith('except '):
        return 'Captura un error y permite manejarlo sin terminar abruptamente.'
    if s.startswith('raise '):
        return 'Lanza una excepción para indicar una condición inválida.'
    if s.startswith('return '):
        return 'Devuelve el resultado de la función al código que la llamó.'
    if s.startswith('continue'):
        return 'Salta a la siguiente iteración del ciclo.'
    if s.startswith('break'):
        return 'Termina el ciclo actual.'
    if s.startswith('with '):
        return 'Abre un contexto que gestiona automáticamente sus recursos.'
    if s.startswith('assert '):
        return 'Verifica una condición que debe cumplirse.'
    if s.startswith('self.') and '=' in s:
        return 'Actualiza el estado interno del objeto mediante un atributo.'
    if s.startswith('result['):
        return 'Guarda información de una fase en el resultado de compilación.'
    if 'emit(' in s:
        return 'Emite una instrucción o un registro para una fase posterior.'
    if 'append(' in s:
        return 'Añade un elemento a una lista de trabajo o resultados.'
    if 'pop(' in s:
        return 'Retira un elemento; en una pila sigue el principio LIFO.'
    if '=' in s and '==' not in s:
        return 'Asigna o actualiza un valor que utilizará el algoritmo.'
    if s in ('}', ']', ')'):
        return 'Cierra una estructura o agrupación abierta previamente.'
    return 'Ejecuta una operación del algoritmo o completa la estructura actual; consultar el bloque de contexto.'


def generate():
    sections = ['# CompilaLab — Guía de lectura línea por línea',
                '', 'Cada entrada conserva el número real de línea del archivo.',
                'Las explicaciones son ayudas de lectura; las decisiones del algoritmo se estudian también con los tests.', '']
    for filename in FILES:
        source = (ROOT / filename).read_text(encoding='utf-8').splitlines()
        sections.extend([f'## `{filename}`', ''])
        for number, line in enumerate(source, 1):
            if not line.strip():
                continue
            # El código se escapa como inline code para no romper la tabla.
            shown = line.replace('`', '\\`').replace('|', '&#124;')
            sections.append(f'**Línea {number}:** `{shown}`  ')
            sections.append(f'**Para qué sirve:** {explain(line)}  ')
            sections.append('')
    OUTPUT.write_text('\n'.join(sections), encoding='utf-8')
    return OUTPUT


if __name__ == '__main__':
    print(generate())
