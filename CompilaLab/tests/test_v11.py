"""Pruebas de las mejoras v11: cada una documenta una regla del curso."""
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compiler import compile_source, lex, CompileError
from automata import identifier_dfa, number_dfa

EXAMPLES = Path(__file__).resolve().parents[1] / 'examples'


class V11Tests(unittest.TestCase):
    def ok(self, source, output, optimized=False):
        r = compile_source(source, optimized=optimized)
        self.assertTrue(r['success'], r.get('error'))
        self.assertEqual(r['output'], output)
        self.assertTrue(r['cpu_matches_tac'])
        return r

    def fails(self, source, phase, fragment):
        r = compile_source(source)
        self.assertFalse(r['success'])
        self.assertEqual(r['error_phase'], phase)
        self.assertIn(fragment, r['error'])
        return r

    # ── S2: léxico ──
    def test_all_lexical_errors_reported(self):
        r = self.fails('int a = 1 @ 2;\nint b = 3 # 4;', 'Léxico', '+1 error')
        self.assertIn('L2:C11', r['error'])

    def test_block_comment_keeps_line_numbers(self):
        tokens = lex('/* uno\ndos */ int x = 1;')
        self.assertEqual((tokens[0].kind, tokens[0].line, tokens[0].column), ('INT', 2, 8))

    def test_unclosed_string_and_comment(self):
        self.fails('string s = "hola;', 'Léxico', 'Cadena sin cerrar')
        self.fails('int a = 1; /* nunca cierra', 'Léxico', 'Comentario')

    def test_keyword_prefix_is_identifier(self):
        # "integer" empieza como la palabra reservada int, pero es UN identificador.
        self.ok('int integer = 4; print(integer);', ['4'])

    def test_dfa_table_rejects(self):
        self.assertEqual(number_dfa('1.2.3').state, 'ERROR')
        self.assertEqual(number_dfa('1.').state, 'punto')
        self.assertFalse(identifier_dfa('2vida').accepted)

    # ── S3-S4: sintaxis ──
    def test_left_associativity(self):
        self.ok('print(10 - 3 - 2);', ['5'])          # (10-3)-2, no 10-(3-2)

    def test_logical_precedence(self):
        # ! > && > ||  →  true || (false && false) = true
        self.ok('print(true || false && false);', ['true'])
        self.ok('print(!false && false);', ['false'])

    def test_logic_example(self):
        self.ok((EXAMPLES / 'logica.clab').read_text(encoding='utf-8'), ['true', 'false'])

    # ── S5: ámbitos ──
    def test_shadowing(self):
        self.ok('int a = 1; fn f() { int a = 2; print(a); } f(); print(a);', ['2', '1'])

    def test_function_cannot_write_global(self):
        self.fails('int a = 5; fn f() { a = 3; } f();', 'Semántico', 'global')

    def test_return_outside_function(self):
        self.fails('return 1;', 'Semántico', 'return fuera')

    # ── S6: tipos ──
    def test_semantic_error_real_column(self):
        r = self.fails('int a = 1;\nstring s = "x";\nint b = a + s;', 'Semántico', 'línea 3')
        self.assertIn('columna 11', r['error'])        # columna del operador '+'

    def test_literal_division_by_zero_is_semantic(self):
        self.fails('float x = 1 / 0;', 'Semántico', 'División por cero')

    def test_variable_division_by_zero_is_runtime(self):
        self.fails('int y = 0; float x = 1 / y;', 'Ejecución', 'división por cero')

    def test_relational_only_numeric(self):
        self.fails('bool b = "a" < "b";', 'Semántico', 'solo entre números')

    def test_not_requires_bool(self):
        self.fails('bool b = !5;', 'Semántico', 'requiere bool')

    # ── S9: optimización ──
    def test_algebraic_simplification(self):
        r = self.ok((EXAMPLES / 'algebraica.clab').read_text(encoding='utf-8'), ['0', '14'], optimized=True)
        notes = ' '.join(r['optimizations'])
        for rule in ('x + 0 = x', '1 * x = x', 'x * 2 = x + x'):
            self.assertIn(rule, notes)

    def test_algebraic_keeps_float_semantics(self):
        # x + 0.0 NO debe simplificarse: cambiaría int → float en la salida.
        r = self.ok('int p = new(4); int q = p - p; float f = q + 0.0; print(f); free(p);', ['0.0'], optimized=True)
        self.assertFalse(any('0 = x' in n for n in r['optimizations']))

    def test_optimized_equals_unoptimized_everywhere(self):
        for path in EXAMPLES.glob('*.clab'):
            source = path.read_text(encoding='utf-8')
            a, b = compile_source(source), compile_source(source, optimized=True)
            self.assertEqual(a.get('output'), b.get('output'), path.name)

    # ── S10: back-end ──
    def test_bool_printed_as_language_literal(self):
        self.ok('print(3 < 4);', ['true'])

    def test_logic_runs_on_cpu_with_spill(self):
        r = self.ok('int a=1; int b=2; int c=3; print(a < b && b < c || a == c);', ['true'])
        self.assertTrue(any(i.startswith(('AND', 'OR')) for i in r['assembly']))


if __name__ == '__main__':
    unittest.main()
