# Guía de sustentación: demostración y preguntas

## Guion de demostración (aprox. 8–12 minutos)

1. **Arquitectura:** explicar la diferencia entre interfaz de usuario y frontend del compilador. La interfaz está en `gui.py`; el motor en `compiler.py`.
2. **Léxico:** mostrar tokens, lexemas, regex, línea y columna; usar la pestaña Autómatas y `automata.py`.
3. **Sintaxis:** explicar la gramática, precedencia y AST; mostrar `(a+b)*c` frente a `a+b*c`.
4. **Semántica:** mostrar símbolos, ámbitos de funciones, compatibilidad de tipos y un error semántico.
5. **IR/TAC:** mostrar cuádruplas y temporales `t1`, `t2`.
6. **Optimización:** activar/desactivar optimización y comparar TAC.
7. **Backend:** mostrar selección de opcodes, R0/R1/R2, liberación de registros y Spill.
8. **Memoria:** mostrar `PUSH/POP`, Heap y direcciones de Spill.
9. **CPU virtual:** navegar las instrucciones y explicar cómo cambian registros y RAM.
10. **Pruebas:** mostrar pruebas automatizadas, un programa correcto, uno con error y uno de estrés.

## Preguntas orientativas (respuestas cortas)

**¿Qué es un compilador?** Traduce un lenguaje fuente a una representación destino, verificando reglas léxicas, sintácticas y semánticas.

**¿Lexer vs Parser?** Lexer agrupa caracteres en tokens; Parser valida la gramática y construye el AST.

**¿Qué es un token?** Categoría de unidad léxica; por ejemplo `NUMBER`, con lexema `123`.

**¿Qué es un autómata finito?** Modelo de estados y transiciones que reconoce patrones; nuestro AFD de demostración reconoce identificadores y números.

**¿Por qué Top-Down?** Porque el parser parte de la regla inicial y desciende recursivamente por producciones; no implementamos LR.

**¿Qué es el AST?** Árbol que representa la estructura esencial del programa, sin todos los signos de la gramática.

**¿Qué es un scope?** Región de visibilidad de identificadores; `lookup()` busca del ámbito local al padre.

**¿Qué es el chequeo de tipos?** Verifica que operaciones y asignaciones respeten tipos compatibles.

**¿Qué es TAC?** Código de tres direcciones, una IR con operaciones simples y temporales.

**¿Por qué optimizar?** Para reducir instrucciones o trabajo manteniendo la semántica observable.

**¿Qué es Stack/LIFO?** La última entrada es la primera salida; se modela con `push()` y `pop()`.

**¿Stack vs Heap?** Stack gestiona marcos de llamada automáticamente; Heap reservas dinámicas explícitas en nuestro simulador.

**¿Qué es Spill?** Guardar un valor vivo de un registro en RAM cuando hay presión de registros; se emite `STORE` y posteriormente `LOAD`.

**¿Qué es liveness?** Determina si un valor todavía será usado en el futuro; nuestro backend usa conteo de usos posteriores, no análisis global de CFG.

**¿Qué es un registro?** Almacenamiento muy rápido y limitado de la CPU; aquí se simula con R0, R1 y R2.

**¿Es ensamblador real?** Es una ISA virtual educativa ejecutada por `VirtualCPU`, no código x86 nativo.

**¿Cómo validan el resultado?** Se ejecuta el TAC y el ensamblador virtual por separado y se comparan las salidas.

**¿Cómo se maneja un error léxico?** En modo pánico: se anota y el escaneo continúa, así el mensaje reporta todos los caracteres inválidos a la vez.

**¿Por qué `int x = 1 / 0;` es error semántico pero `1 / y` no?** El divisor literal se conoce al compilar; el valor de `y` solo se conoce al ejecutar.

**¿Qué es la reducción de fuerza?** Cambiar una operación cara por una equivalente más barata: `x * 2` pasa a `x + x`.

**¿Por qué no se simplifica `x + 0.0`?** Porque si `x` es `int`, el resultado cambiaría a `float` y se imprimiría distinto: una optimización no puede cambiar lo observable.

**¿Qué es caller-saved?** Antes de un `CALL`, el llamador guarda en RAM los valores que necesitará después, porque la función puede usar cualquier registro.

**¿Qué no implementa el proyecto?** Java completo, LR/LALR, SSA, coloreado de grafos, `if`/`while` con saltos en la IR, hardware físico y parámetros de funciones.
