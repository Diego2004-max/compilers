"""Interfaz de consola: el mismo compile_source() que usa la GUI, impreso fase por fase.

Ejemplo:  python main.py examples/spill.clab --registers 3
          python main.py examples/algebraica.clab --optimize
"""
import argparse
import json
from pathlib import Path
from compiler import compile_source

BASE=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser(description='CompilaLab — compilador educativo')
    p.add_argument('file',nargs='?',default=str(BASE/'examples'/'correcto.clab'))
    p.add_argument('--registers',type=int,default=3)
    p.add_argument('--optimize',action='store_true')
    p.add_argument('--json',action='store_true')
    a=p.parse_args()
    if a.registers<3: p.error('Se requieren al menos 3 registros para esta ISA virtual')
    source=Path(a.file).read_text(encoding='utf-8')
    r=compile_source(source,a.registers,a.optimize)
    if a.json: print(json.dumps(r,indent=2,ensure_ascii=False)); return
    print('=== CÓDIGO FUENTE ===\n'+source)
    for key,title in [('tokens','TOKENS'),('ast','AST'),('symbols','TABLA DE SÍMBOLOS'),('tac','TAC'),('optimized_tac','TAC OPTIMIZADO'),('optimizations','OPTIMIZACIONES'),('assembly','ENSAMBLADOR VIRTUAL'),('register_events','REGISTROS Y SPILL'),('memory_events','MEMORIA STACK/HEAP'),('output','SALIDA')]:
        if key in r: print(f'\n=== {title} ===\n'+(json.dumps(r[key],indent=2,ensure_ascii=False) if key in ('tokens','ast','symbols') else '\n'.join(map(str,r[key]))))
    print(f'\nSPILLS: {r.get("spill_count",0)}')
    print('OK' if r['success'] else f"ERROR [{r.get('error_phase')}]: {r['error']}")

if __name__=='__main__': main()
