# CompilaLab — Mapa teoría ↔ código (auditoría inicial)

**Estados:** IMPLEMENTADO = existe comportamiento verificable; PARCIAL = solo subconjunto/simulación; PENDIENTE = no implementado. Este documento es una auditoría, no una afirmación de cobertura total.

| Semana | Tema del curso | Archivo / función | Estado | Próximo paso |
|---|---|---|---|---|
| 1 | Pipeline del compilador | `compiler.py:compile_source` | IMPLEMENTADO | Separar módulos por etapas |
| 2 | Tokens, lexemas y regex | `compiler.py:PATTERN`, `lex` | IMPLEMENTADO | Añadir visualización de autómata y casos límite |
| 2 | Autómatas léxicos | — | PENDIENTE | DFA didáctico con transiciones |
| 3 | Gramática BNF/EBNF | `Parser` (gramática implícita) | PARCIAL | Documentar gramática formal |
| 3–4 | Parser Top-Down y AST | `Parser`, `Node` | IMPLEMENTADO | Dibujar AST como árbol |
| 4 | Bottom-Up, comparación de métodos | — | PENDIENTE | Demostración comparativa sin cambiar parser principal |
| 5 | Tabla de símbolos y scopes | `Semantic` | PARCIAL | Bloques anidados y visibilidad real |
| 6 | Tipos y errores semánticos | `Semantic.expr`, `Semantic.block` | PARCIAL | Más operaciones y punteros tipados |
| 7 | IR / TAC / cuádruplas | `IRBuilder`, `Quad` | IMPLEMENTADO | Saltos y control de flujo |
| 8 | Stack frames y LIFO | `Memory.push/pop`, `Interpreter` | IMPLEMENTADO (simulado) | Recursión con límite |
| 8 | Heap / alloc / free | `Memory.alloc/free` | IMPLEMENTADO (simulado) | Liberación y referencias inválidas |
| 8 | Segmentos Texto/Data/Stack/Heap | — | PARCIAL | Visualizador de segmentos |
| 9 | Propagación y plegado constantes | `optimize` | IMPLEMENTADO (local) | Optimización por bloques básicos |
| 9 | Simplificación algebraica | — | PENDIENTE | Reglas `x+0`, `x*1`, etc. |
| 9 | Código muerto | — | PENDIENTE | Análisis de usos y efectos laterales |
| 10 | Código objetivo | `Backend.generate` | IMPLEMENTADO (ISA virtual) | Máquina virtual para ejecutar ASM |
| 10 | Asignación de registros | `Backend.reg` | PARCIAL | Liveness y estrategia de selección sólida |
| 10 | Spill / STORE / LOAD | `Backend.reg` | PARCIAL | Validación semántica del ensamblador emitido |
| 10 | Coloreado de grafos | — | PENDIENTE | Comparador didáctico opcional |

## Condición para afirmar que está terminado

1. El caso correcto produce el mismo resultado en intérprete TAC y máquina virtual ASM.
2. Cada error léxico, sintáctico y semántico indica línea y columna cuando sea posible.
3. Los escenarios de Spill se ejecutan y verifican, no solo muestran trazas.
4. Cada tema del curso está enlazado a código, una prueba y una explicación para sustentación.

## Arquitectura objetivo

`gui.py` (interfaz) → `compiler_service` (orquestación) → `compiler/frontend` (lexer/parser/semántica) → `compiler/middle_end` (IR/optimizador) → `compiler/backend` (registros, spill, memoria, código objetivo).

**Nota:** los nombres frontend/backend dentro de `compiler/` se refieren a fases de compilación; la GUI es el frontend de la aplicación.

## Actualización v3 — Ejecución del código objetivo

- `virtual_cpu.py`: decodificación y ejecución de `LI`, `MOV`, `STORE`, `LOAD`, `ADD`, `SUB`, `MUL`, `DIV`, comparaciones, `PRINT`, `ENTER`, `LEAVE`, `CALL`, `RET`, `ALLOC` y `FREE`.
- `compiler.py`, `compile_source()`: compara automáticamente salida de la CPU virtual con la del intérprete TAC.
- `compiler.py`, `Backend.generate()`: conservación de valores vivos alrededor de `CALL` mediante slots RAM, evitando la pérdida de punteros globales.
- `gui.py`: nueva pestaña **CPU virtual** con traza, registros, RAM y verificación de salida.
- `tests/test_cpu_virtual.py`: pruebas de Spill, llamadas, Heap, aritmética, comparación y optimización.

La pila de marcos es lógica; no se debe presentar como un stack físico modelado byte a byte. El archivo `virtual_cpu.py` no ejecuta código de máquina nativo.
