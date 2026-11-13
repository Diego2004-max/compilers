# CompilaLab v11 — Proyecto integral de Construcción de Compiladores

Aplicación educativa de escritorio que reúne el pipeline **código fuente → tokens → AST → análisis semántico → TAC → optimización → ensamblador virtual → CPU/RAM virtuales**.

## Ejecutar en Windows con Python 3.10+

```powershell
cd CompilaLab
python gui.py
```

No requiere paquetes externos; usa `tkinter`, `unittest` y bibliotecas estándar de Python.

## Panel web para la presentación

```powershell
python dashboard.py
```

Abre el navegador en `http://127.0.0.1:8765` (sin internet ni paquetes externos) con tres secciones:

- **Pipeline:** cinta de 7 fases con sus métricas; tokens y AFD, árbol AST dibujado, tabla de símbolos, cuádruplas, optimización antes/después, ensamblador con spills y CPU paso a paso (flechas ← → del teclado). Los errores marcan la línea y la columna con `^`.
- **Rendimiento:** tiempo por fase (mediana), spills según número de registros, tamaño del código por programa y escalabilidad del back-end.
- **Arquitectura:** diagrama de módulos, tamaño del código, tecnologías detectadas en el equipo y decisiones de diseño.

## Ejecutar pruebas

```powershell
python -m unittest discover -s tests -v
```

## Uso

1. Elegir ejemplo: **Correcto**, **Spill**, **Tipos**, **Léxico**, **Stack / Heap**, **Optimiz.**, **Algebraica** o **Lógica**.
2. Establecer registros en **3**; desmarcar optimización para demostrar Spill.
3. Presionar **Compilar y ejecutar**.
4. Inspeccionar las pestañas Tokens, Autómatas, Gramática, AST, Símbolos, TAC, Optimización, Ensamblador, Spill, Memoria, CPU virtual, Paso a paso, Cobertura y Salida.
5. En **Paso a paso**, usar los botones **◀ CPU** y **CPU ▶** para recorrer la traza de instrucciones.

## Estructura

- `gui.py`: interfaz gráfica de escritorio (Tkinter).
- `dashboard.py` + `web/`: panel web local para la presentación.
- `compiler.py`: lexer, parser, AST, semántica, TAC, optimizador, asignación de registros, Spill, memoria y compilación.
- `automata.py`: AFD didácticos para identificadores/números y gramática visible.
- `virtual_cpu.py`: CPU virtual y ejecución del ensamblador.
- `coverage.py`: matriz de cobertura teoría-código con estados explícitos.
- `examples/`: programas de prueba.
- `tests/`: pruebas automáticas.
- `docs/TEORIA_Y_LIMITACIONES.md`: relación con semanas 1–10 y alcance real.
- `docs/GUIA_SUSTENTACION.md`: demostración y preguntas.

## Sintaxis de ejemplo

```c
int a = 5;
int b = 10;
int c = 2;
int resultado = a + b * c;
print(resultado);
```

Admite declaraciones `int`, `float`, `string`, `bool`, asignaciones, expresiones aritméticas, comparaciones y lógicas (`&&`, `||`, `!`), comentarios `//` y `/* */`, `print`, funciones sin parámetros, `return`, `new(n)` y `free(p)`. No es Java completo.

## Resultado de referencia

El ejemplo `spill.clab` imprime `92` y, con tres registros sin optimización, genera eventos de Spill. El ensamblador generado se ejecuta en una CPU **virtual**, no física. Las pruebas comprueban concordancia de salidas TAC/CPU.

## Advertencia sobre el alcance

**v11** identifica la entrega integral para estudiar el curso, **no significa que todos los algoritmos teóricos estén implementados**. Ver `docs/TEORIA_Y_LIMITACIONES.md` y la pestaña Cobertura: se diferencian explícitamente implementaciones, simulaciones, coberturas parciales y temas solo teóricos.

## Ampliación: backend de ejecutables reales

El botón **«Ejecutable REAL (GCC/Clang)»** añade una ruta de compilación nativa: código CompilaLab → Lexer → Parser → AST → Semántica → C11 → GCC/Clang → ejecutable de la plataforma → salida del proceso. Esta ruta **no utiliza la CPU virtual**. Necesita instalar GCC o Clang y añadirlo al PATH del sistema. Para inspeccionar el código generado, abrir la pestaña **C nativo**.

**Limitaciones importantes:** la generación de código nativo todavía no admite `new/free`, funciones con retorno ni funciones que lean variables locales de `main`. La interfaz didáctica de CPU/RAM y Spill continúa siendo virtual. Consulta `docs/ESTADO_REAL_Y_PENDIENTES.md` antes de presentar el proyecto. No se afirma que todas las técnicas del semestre estén implementadas.

## Guía comentada

**Lo principal para estudiar son los comentarios dentro del código:** `[S#]` indica la semana del curso y `(?)` una pregunta probable de sustentación con la idea clave para responderla.

`docs/CODIGO_LINEA_POR_LINEA.md` contiene cada línea no vacía del código Python con una explicación asociada. Se genera mediante `python generar_guia_comentada.py`. Es una guía de lectura; algunas explicaciones son generales y requieren contrastarse con la función completa.
