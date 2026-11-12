# Auditoría honesta del proyecto — backend nativo

## Qué es real

- El análisis léxico, sintáctico, AST, análisis semántico, TAC y optimización son algoritmos Python reales.
- El nuevo backend `native_backend.py` **traduce AST a C11** y llama a un compilador de sistema **GCC o Clang** para producir un ejecutable nativo de la plataforma.
- La salida de la pestaña «Salida nativa» procede del **proceso ejecutable real**, no del intérprete Python ni de la CPU virtual.
- La selección real de instrucciones, asignación física de registros y spilling de este ejecutable son responsabilidad de GCC/Clang. Para estudiarlos, se puede inspeccionar el ensamblador del compilador (`gcc -S -O0 programa.c -o programa.s`).
- Las pruebas `test_native_backend.py` compilan y ejecutan programas de verdad si GCC/Clang está disponible.

## Qué sigue siendo virtual o parcial

- Las pestañas «Ensamblador», «Spill», «Memoria», «CPU virtual» y «Paso a paso» siguen correspondiendo al backend didáctico de una ISA virtual. **No representan las instrucciones físicas del ejecutable nativo**.
- `new` y `free` no se admiten en el backend nativo actual; el sistema muestra un error explícito. Se mantienen en la vía didáctica.
- Funciones con `return` y funciones que acceden a variables locales de `main` no están soportadas por el backend nativo actual.
- El frontend no implementa todas las gramáticas y estrategias de parsing del curso (por ejemplo, LR/LALR), ni el asignador global por coloreado de grafos.
- El lenguaje no tiene `if`/`while`, así que la IR no tiene saltos condicionales y todas las optimizaciones son locales (un solo bloque básico por función).
- Los `float` se imprimen distinto en las dos rutas: la virtual muestra `3.0` (formato Python) y la nativa `3` (`%.15g` de C). Los `bool` ya se imprimen igual (`true`/`false`).
- La interfaz gráfica Tkinter no se considera un frontend del compilador; es la interfaz de usuario.
- No se puede garantizar el 100 % de la teoría de las diapositivas como funcionalidades ejecutables con el alcance actual.

## Dependencia en Windows

Instalar GCC (por ejemplo mediante MSYS2/MinGW-w64) o LLVM/Clang y asegurarse de que `gcc --version` o `clang --version` funciona en la terminal de VS Code. No se incluye ningún compilador de terceros en el ZIP.

## Cómo ejecutar

- `python gui.py`: abre el proyecto completo.
- «Compilar y ejecutar»: ejecuta la ruta educativa de IR/TAC/CPU virtual.
- «Ejecutable REAL (GCC/Clang)»: genera C11, compila un binario real y ejecuta ese binario.
- `python -m unittest discover -s tests -v`: ejecuta pruebas (las nativas se omiten si no hay GCC/Clang).
- `python generar_guia_comentada.py`: regenera la guía de lectura línea por línea.

## Nota de seguridad

Los programas fuente se traducen desde un AST validado, pero ejecutar código compilado sigue ejecutando un proceso local. Usar solamente programas de confianza, y no ejecutar ejemplos desconocidos con permisos elevados.
