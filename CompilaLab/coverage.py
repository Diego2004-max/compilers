"""Matriz teoría ↔ código: trazabilidad pedagógica, no certificación industrial.

Estados:  Implementado = el algoritmo se ejecuta y tiene pruebas.
          Simulación   = modelo educativo (no hardware ni SO real).
          Parcial      = solo un subconjunto del concepto.
          Solo teoría  = se explica, no se ejecuta.
"""
COVERAGE = [
 ('1','Arquitectura por fases (front/middle/back-end)','compiler.compile_source','Implementado'),
 ('1','Clasificación de errores por fase','compiler.CompileError / error_phase','Implementado'),
 ('2','Tokens, lexemas, patrones (regex con named groups)','compiler.PATTERN / lex','Implementado'),
 ('2','Recuperación de errores léxicos (modo pánico)','compiler.lex','Implementado'),
 ('2','Comentarios //, /* */ y cadenas (reto S2)','compiler.PATTERN','Implementado'),
 ('2','AFD por matriz de transición','automata.run_dfa / *_TABLE','Implementado (didáctico)'),
 ('2','Thompson, subconjuntos, Hopcroft','docs/TEORIA_Y_LIMITACIONES.md','Solo teoría'),
 ('3','Gramática libre de contexto (EBNF)','automata.GRAMMAR','Implementado'),
 ('3-4','Descenso recursivo Top-Down y AST','compiler.Parser / Node','Implementado'),
 ('4','Precedencia y asociatividad sin recursión izquierda','compiler.Parser.binary_level','Implementado'),
 ('4','Bottom-Up shift-reduce, LR/LALR','docs/TEORIA_Y_LIMITACIONES.md','Solo teoría'),
 ('5','Tabla de símbolos, pila de ámbitos, lookup','compiler.Semantic','Implementado'),
 ('5','Shadowing local/global y redeclaración','compiler.Semantic.block','Implementado'),
 ('5','Ámbitos de bloque (if/while)','—','Parcial (el lenguaje no tiene bloques)'),
 ('6','Inferencia, equivalencia y coerción int→float','compiler.Semantic.expr / compatible','Implementado'),
 ('6','División por cero con divisor literal','compiler.Semantic.expr','Implementado'),
 ('7','TAC, cuádruplas y temporales','compiler.IRBuilder / Quad','Implementado'),
 ('7','Saltos condicionales (GOTO) en la IR','—','Solo teoría'),
 ('8','Stack LIFO, Stack Frames y Heap','compiler.Memory','Simulación'),
 ('9','Simplificación algebraica y reducción de fuerza','compiler.simplify_algebraic','Implementado'),
 ('9','Propagación y plegado de constantes','compiler.optimize','Implementado'),
 ('9','Eliminación de temporales muertos','compiler.eliminate_dead_temporaries','Implementado'),
 ('9','Optimización global sobre CFG','docs/TEORIA_Y_LIMITACIONES.md','Solo teoría'),
 ('10','Selección de instrucciones, ensamblador','compiler.Backend','Implementado (ISA virtual)'),
 ('10','Asignación local de registros, liveness aproximado y Spill','compiler.Backend.reg','Implementado'),
 ('10','Coloreado de grafos (Chaitin-Briggs)','docs/TEORIA_Y_LIMITACIONES.md','Solo teoría'),
 ('10','CPU virtual fetch-decode-execute y RAM de Spill','virtual_cpu.VirtualCPU','Simulación'),
 ('10','Ejecutable nativo vía C11 + GCC/Clang','native_backend.build_native','Implementado (parcial)'),
 ('10','Pruebas del pipeline y validación TAC vs CPU','tests/','Implementado'),
]
