"""Panel web local de CompilaLab: pipeline interactivo, rendimiento y arquitectura.

Uso:   python dashboard.py            (abre el navegador en http://127.0.0.1:8765)
       python dashboard.py --no-browser --port 9000

Solo biblioteca estándar: http.server sirve la carpeta web/ y una pequeña API JSON
que llama al MISMO compile_source() que usan gui.py y main.py. No necesita internet.
Escucha únicamente en 127.0.0.1: nadie fuera de este equipo puede enviarle código.

(?) ¿Por qué un servidor y no solo un HTML? El compilador está en Python; el
    navegador no puede ejecutarlo. El servidor es el puente: el HTML envía el
    código fuente y recibe el resultado de cada fase como JSON.
"""
from __future__ import annotations

import argparse
import json
import platform
import re
import statistics
import sys
import webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from compiler import compile_source
from native_backend import find_compiler

BASE = Path(__file__).resolve().parent
WEB = BASE / 'web'
EXAMPLES = BASE / 'examples'
PHASES = ['lexico', 'sintactico', 'semantico', 'ir', 'optimizacion', 'backend', 'interprete', 'cpu']
MODULES = ['compiler.py', 'automata.py', 'virtual_cpu.py', 'native_backend.py',
           'gui.py', 'main.py', 'dashboard.py', 'coverage.py']
MAX_SOURCE = 20_000          # caracteres: evita que un pegado accidental congele el servidor


def examples():
    return {p.stem: p.read_text(encoding='utf-8') for p in sorted(EXAMPLES.glob('*.clab'))}


def code_lines(path):
    """Líneas de código reales: sin vacías y sin comentarios de línea completa."""
    lines = path.read_text(encoding='utf-8').splitlines()
    return sum(1 for l in lines if l.strip() and not l.strip().startswith('#'))


def scaling_program(n):
    """Programa sintético con n variables y una suma de n términos: estresa registros y spill."""
    decls = '\n'.join(f'int v{i} = {i + 1};' for i in range(n))
    total = ' + '.join(f'v{i}' for i in range(n))
    return f'{decls}\nint r = {total};\nprint(r);\n'


def timed(source, repeats, **opts):
    """Mediana por fase en `repeats` corridas: la mediana ignora picos del sistema operativo."""
    runs = [compile_source(source, **opts) for _ in range(repeats)]
    if not runs[-1]['success']:
        return runs[-1], {}
    phases = {ph: statistics.median(r['timings'].get(ph, 0.0) for r in runs) for ph in PHASES}
    return runs[-1], phases


def benchmark(payload):
    repeats = max(1, min(int(payload.get('repeats', 15)), 60))
    name = payload.get('example', 'spill')
    progs = examples()
    source = progs.get(name, progs['spill'])

    last, phases = timed(source, repeats)
    out = {'example': name, 'repeats': repeats, 'success': last['success'], 'error': last.get('error'),
           'phases': phases, 'total_ms': sum(phases.values())}

    # Spills según número de registros, con y sin optimización.
    out['registers'] = []
    for regs in range(3, 9):
        a = compile_source(source, registers=regs, optimized=False, run=False)
        b = compile_source(source, registers=regs, optimized=True, run=False)
        out['registers'].append({'registers': regs,
                                 'sin_optimizar': a.get('spill_count'), 'optimizado': b.get('spill_count')})

    # Tamaño de código por ejemplo (solo los que compilan).
    out['sizes'] = []
    for ex_name, ex_src in progs.items():
        r = compile_source(ex_src, run=False)
        if r['success']:
            o = compile_source(ex_src, optimized=True, run=False)
            out['sizes'].append({'example': ex_name,
                                 'tac': len(r['tac']), 'tac_opt': len(r['optimized_tac']),
                                 'asm': len(r['assembly']), 'asm_opt': len(o['assembly'])})

    # Escalabilidad: tiempo total y del back-end frente al tamaño del programa.
    out['scaling'] = []
    for n in (10, 25, 50, 100, 150, 200):
        r, ph = timed(scaling_program(n), 3)
        out['scaling'].append({'n': n, 'total': sum(ph.values()), 'backend': ph.get('backend', 0.0),
                               'quads': len(r.get('tac', [])), 'spills': r.get('spill_count')})
    return out


def system_info():
    tests_src = '\n'.join(p.read_text(encoding='utf-8') for p in (BASE / 'tests').glob('test_*.py'))
    return {
        'python': platform.python_version(),
        'platform': f'{platform.system()} {platform.release()}',
        'c_compiler': find_compiler(),
        'modules': [{'file': m, 'lines': code_lines(BASE / m)}
                    for m in MODULES if (BASE / m).exists()],
        'test_count': len(re.findall(r'^\s*def test_', tests_src, re.M)),
        'examples': len(list(EXAMPLES.glob('*.clab'))),
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB), **kwargs)

    def log_message(self, fmt, *args):           # consola limpia durante la presentación
        pass

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, default=str).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get('Content-Length', 0))
        if length > MAX_SOURCE * 4:
            raise ValueError('Solicitud demasiado grande')
        return json.loads(self.rfile.read(length) or b'{}')

    def do_GET(self):
        if self.path == '/api/examples':
            return self.send_json(examples())
        if self.path == '/api/system':
            return self.send_json(system_info())
        if self.path in ('/', ''):
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        try:
            payload = self.read_json()
            if self.path == '/api/compile':
                source = str(payload.get('source', ''))[:MAX_SOURCE]
                registers = max(3, min(int(payload.get('registers', 3)), 16))
                return self.send_json(compile_source(source, registers, bool(payload.get('optimized'))))
            if self.path == '/api/benchmark':
                return self.send_json(benchmark(payload))
            return self.send_json({'error': 'Ruta no encontrada'}, 404)
        except Exception as error:               # el panel muestra el error; el servidor sigue vivo
            return self.send_json({'error': f'{type(error).__name__}: {error}'}, 500)


def main():
    parser = argparse.ArgumentParser(description='Panel web local de CompilaLab')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    server = None
    for port in range(args.port, args.port + 10):    # si el puerto está ocupado, prueba los siguientes
        try:
            server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
            break
        except OSError:
            continue
    if server is None:
        sys.exit('No hay puertos libres entre %d y %d' % (args.port, args.port + 9))
    url = f'http://127.0.0.1:{server.server_address[1]}/'
    print(f'CompilaLab panel en {url}  (Ctrl+C para detener)')
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nPanel detenido.')


if __name__ == '__main__':
    main()
