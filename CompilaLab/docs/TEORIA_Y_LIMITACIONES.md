# CompilaLab v10 — Teoría del curso y alcance real

Este documento distingue tres estados: **implementado** (el programa ejecuta el algoritmo), **simulado** (modelo educativo, no hardware real) y **solo teoría** (comparación y explicación, no algoritmo ejecutado).

## Semanas 1–2: arquitectura, tokens y autómatas

- El pipeline `compile_source()` en `compiler.py` conecta léxico, sintaxis, semántica, TAC, optimización, ensamblador y CPU virtual.
- `lex()` aplica una expresión regular maestra; produce tokens con lexema, línea y columna, descarta comentarios y espacios y detecta caracteres inválidos.
- `automata.py` contiene **AFD de demostración** para reconocer identificadores y números; su traza permite observar estados, transiciones y aceptación. **La tokenización de producción usa Regex**, no el AFD de demostración.
- AFN, epsilon-transiciones, conversión AFN→AFD y minimización son conceptos estudiables pero **no están implementados** como algoritmos genéricos.

## Semanas 3–4: gramáticas, análisis sintáctico y AST

- `automata.GRAMMAR` describe la gramática de las construcciones soportadas.
- `Parser` usa **descenso recursivo (Top-Down)** con `comparison`, `add`, `mul`, `unary`, `atom`, respetando precedencia.
- `Node` representa el AST; la interfaz lo muestra como JSON estructurado.
- La sintaxis de CompilaLab es un subconjunto educativo de lenguajes estilo C/Java, **no es Java completo**.
- **No se implementan** parsers Bottom-Up, tablas LR, SLR ni LALR; son enfoques alternativos de la teoría.

## Semana 5: tabla de símbolos y ámbitos

- `Semantic` contiene una pila de ámbitos y `lookup()` busca desde el ámbito actual hacia el padre.
- Detecta variables inexistentes, redeclaraciones y funciones inexistentes.
- Las funciones sin parámetros generan ámbitos locales. **No se soportan** bloques arbitrarios `if`/`while`, parámetros, shadowing completo ni funciones recursivas; la pila de ámbitos se usa de forma limitada.

## Semana 6: tipos

- `Semantic.expr()` verifica tipos `int`, `float`, `string`, `bool`, operadores numéricos y comparaciones.
- Se permite asignar `int` a `float`; `new()` devuelve una dirección de heap que en este lenguaje se almacena en un `int` (puntero didáctico).
- Los errores semánticos reportan la línea; la columna semántica no siempre es exacta.

## Semana 7: IR / TAC

- `IRBuilder` traduce AST a cuádruplas `Quad(op, a, b, dest, line)` y temporales `t1`, `t2`...
- La pestaña TAC presenta la forma legible y la API devuelve `quads` estructurados.
- Diferencia: AST expresa estructura del programa; TAC explicita operaciones simples independientes de la ISA.

## Semanas 8–9: memoria y optimización

- `Memory` usa lista para Stack LIFO y diccionario para Heap con direcciones ficticias `0x1000` en adelante.
- `push()` y `pop()` simulan Stack Frames; `alloc()` y `free()` simulan reserva/liberación. Se detecta doble liberación.
- La CPU virtual usa RAM `dict` para los slots de Spill desde `0x2000`; se puede inspeccionar la traza por instrucción.
- `optimize()` realiza propagación y plegado de constantes. `eliminate_dead_temporaries()` elimina definiciones puras de temporales sin uso en programas sin llamadas.
- **No se implementan** análisis global de flujo de datos, SSA, bucles, GC, memoria física, segmentación real ni detección general de fugas.

## Semana 10: generación de código objetivo

- `Backend` traduce TAC a **ensamblador de ISA virtual**, con `LI`, `MOV`, `ADD`, `SUB`, `MUL`, `DIV`, comparaciones, `LOAD`, `STORE`, `PRINT`, `ENTER`, `LEAVE`, `CALL`, `RET`, `ALLOC`, `FREE`.
- Asigna registros `R0...Rn`, libera valores sin usos futuros y, ante presión, hace Spill con `STORE` y posterior `LOAD`.
- `VirtualCPU` ejecuta las instrucciones y compara la salida con la ejecución de TAC. Su traza contiene registros, RAM, pila y heap.
- **No genera binarios x86/ARM/MIPS/RISC-V**, no implementa coloreado de grafos, no calcula liveness mediante CFG y no ejecuta en la CPU física.

## Limitaciones importantes para una sustentación rigurosa

1. El objetivo es **un compilador educativo integrado y ejecutable** con una ISA propia, no un compilador industrial ni un intérprete de Java.
2. La cobertura de la teoría **no implica implementar todos los algoritmos alternativos** explicados en clase.
3. Los errores semánticos de división por cero pueden detectarse durante ejecución de TAC o CPU; son errores de ejecución, no siempre errores semánticos estáticos.
4. El modelo de Stack Frame no equivale a la pila real del sistema operativo. Los slots de Spill son direcciones virtuales del simulador.
5. El modelo de funciones es básico (sin parámetros); para ejemplos complejos usar expresiones, variables, llamadas sin argumentos y `new/free`.
6. Si un ejemplo produce error, no se debe afirmar que la compilación fue exitosa; consultar el campo `error` y su fase.

## Ruta para estudiar con el código

1. Ejecutar `examples/correcto.clab`; inspeccionar Tokens → AST → Símbolos → TAC → Ensamblador → CPU virtual.
2. Abrir `automata.py`, probar `identifier_dfa('x2')` y `number_dfa('3.14')`; observar transiciones.
3. Cambiar una expresión con paréntesis y comparar AST/TAC.
4. Ejecutar `examples/tipos_error.clab` y explicar la tabla de símbolos y la incompatibilidad.
5. Ejecutar `examples/optimizacion.clab` con y sin optimización; comparar instrucciones.
6. Ejecutar `examples/spill.clab` con 3 registros y sin optimización; seguir `STORE`/`LOAD` en RAM.
7. Ejecutar `examples/memoria.clab` y explicar LIFO, Stack Frames, `new` y `free`.
8. Abrir la pestaña **Paso a paso** y navegar la traza de la CPU virtual.
9. Ejecutar `python -m unittest discover -s tests -v` y explicar qué valida cada prueba.
