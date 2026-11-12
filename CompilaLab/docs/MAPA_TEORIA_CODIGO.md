# CompilaLab v11 — Mapa teoría ↔ código

**Estados:** IMPLEMENTADO = comportamiento ejecutable con prueba; SIMULACIÓN = modelo educativo; PARCIAL = subconjunto; SOLO TEORÍA = se explica, no se ejecuta.
Los comentarios dentro del código usan las mismas referencias: `[S#]` = semana del curso y `(?)` = pregunta probable en la sustentación.

| Semana | Tema del curso | Archivo / función | Estado | Prueba que lo demuestra |
|---|---|---|---|---|
| 1 | Pipeline por fases | `compiler.py:compile_source` | IMPLEMENTADO | todas |
| 1 | Clasificación de errores por fase | `CompileError`, `result['error_phase']` | IMPLEMENTADO | `test_v11.fails(...)` |
| 2 | Tokens, lexemas, patrones (regex + named groups) | `PATTERN`, `lex` | IMPLEMENTADO | `test_lexical`, `test_keyword_prefix_is_identifier` |
| 2 | Recuperación de errores léxicos (modo pánico) | `lex` (lista `errors`) | IMPLEMENTADO | `test_all_lexical_errors_reported` |
| 2 | Reto S2: comentarios `//` `/* */`, cadenas, `&& \|\| !` | `PATTERN` | IMPLEMENTADO | `test_block_comment_keeps_line_numbers` |
| 2 | AFD por matriz de transición | `automata.py:run_dfa`, `*_TABLE` | IMPLEMENTADO (didáctico) | `test_dfa_table_rejects` |
| 2 | Thompson / subconjuntos / Hopcroft | — | SOLO TEORÍA | — |
| 3 | Gramática EBNF | `automata.GRAMMAR` | IMPLEMENTADO | `test_grammar` |
| 3–4 | Descenso recursivo y AST | `Parser`, `Node` | IMPLEMENTADO | `test_precedence`, `test_parentheses` |
| 4 | Precedencia y asociatividad izquierda | `Parser.binary_level` | IMPLEMENTADO | `test_left_associativity`, `test_logical_precedence` |
| 4 | Bottom-Up (shift-reduce, LR/LALR) | — | SOLO TEORÍA | — |
| 5 | Pila de ámbitos y `lookup` | `Semantic.scopes`, `Semantic.lookup` | IMPLEMENTADO | `test_undefined`, `test_shadowing` |
| 5 | Redeclaración y shadowing | `Semantic.block` | IMPLEMENTADO | `test_scope_redeclaration_rejected` |
| 5 | Ámbitos de bloque `if`/`while` | — | PARCIAL (el lenguaje no tiene bloques) | — |
| 6 | Inferencia, equivalencia, coerción int→float | `Semantic.expr`, `Semantic.compatible` | IMPLEMENTADO | `test_type_error`, `test_float` |
| 6 | División por cero literal (estática) | `Semantic.expr` | IMPLEMENTADO | `test_literal_division_by_zero_is_semantic` |
| 7 | TAC, cuádruplas, temporales | `IRBuilder`, `Quad` | IMPLEMENTADO | `test_correct` |
| 7 | Saltos/GOTO en la IR | — | SOLO TEORÍA | — |
| 8 | Stack frames LIFO, Heap, doble free | `Memory` | SIMULACIÓN | `test_memory`, `test_double_free` |
| 9 | Simplificación algebraica y reducción de fuerza | `simplify_algebraic` | IMPLEMENTADO | `test_algebraic_simplification` |
| 9 | Propagación y plegado de constantes | `optimize` | IMPLEMENTADO | `test_constant_optimization` |
| 9 | Código muerto (temporales) | `eliminate_dead_temporaries` | IMPLEMENTADO | `test_dead_temporaries` |
| 9 | Optimización global sobre CFG | — | SOLO TEORÍA | — |
| 10 | Selección de instrucciones | `Backend.generate`, `OPCODES` | IMPLEMENTADO (ISA virtual) | `test_arithmetic` |
| 10 | Asignación local de registros + Spill | `Backend.reg`, `release_dead` | IMPLEMENTADO | `test_spill_cpu_ram` |
| 10 | Caller-saved antes de CALL | `Backend.generate` (rama CALL) | IMPLEMENTADO | `test_memory_and_call` |
| 10 | Coloreado de grafos | — | SOLO TEORÍA | — |
| 10 | Ejecución fetch-decode-execute | `virtual_cpu.VirtualCPU` | SIMULACIÓN | `test_cpu_virtual.*` |
| 10 | Ejecutable real (C11 + GCC/Clang) | `native_backend.build_native` | IMPLEMENTADO (parcial) | `test_native_backend.*` |

## Arquitectura

`gui.py` / `main.py` (interfaces de usuario) → `compiler.compile_source` (orquestador) →
front-end (`lex`, `Parser`, `Semantic`) → middle-end (`IRBuilder`, `optimize`) → back-end (`Backend`, `VirtualCPU` o `native_backend`).

Los nombres front-end/back-end se refieren a **fases de compilación**; la GUI es solo la interfaz.
