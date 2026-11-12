import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from compiler import compile_source
from automata import identifier_dfa,number_dfa,GRAMMAR
from coverage import COVERAGE

class ComprehensiveTests(unittest.TestCase):
    def compile_ok(self,source,output=None,optimized=False):
        r=compile_source(source,optimized=optimized)
        self.assertTrue(r['success'],r.get('error'))
        self.assertTrue(r['cpu_matches_tac'])
        if output is not None: self.assertEqual(r['output'],output)
        return r
    def test_identifier_dfa(self):
        for x in ['a','_x2','valor_22']: self.assertTrue(identifier_dfa(x).accepted)
        for x in ['','2a','a-b']: self.assertFalse(identifier_dfa(x).accepted)
    def test_number_dfa(self):
        for x in ['0','12','12.5']: self.assertTrue(number_dfa(x).accepted)
        for x in ['','1.','a','1.2.3']: self.assertFalse(number_dfa(x).accepted)
    def test_grammar(self): self.assertIn('comparison',GRAMMAR)
    def test_automata_trace(self):
        r=self.compile_ok('int hola_2 = 12; print(hola_2);',['12'])
        self.assertTrue(any(x['lexema']=='hola_2' for x in r['automata']))
    def test_precedence(self): self.compile_ok('print(2 + 3 * 4);',['14'])
    def test_parentheses(self): self.compile_ok('print((2 + 3) * 4);',['20'])
    def test_unary(self): self.compile_ok('print(-3 + 4);',['1'])
    def test_float(self): self.compile_ok('float a = 2.5; print(a + 0.5);',['3.0'])
    def test_string(self): self.compile_ok('string a = "Hola"; print(a);',['Hola'])
    def test_boolean(self): self.compile_ok('bool a = 3 <= 4; print(a);',['True'])
    def test_lex_error_location(self):
        r=compile_source('int a = 1;\nint b = @;')
        self.assertFalse(r['success']); self.assertIn('línea 2',r['error'])
    def test_syntax_error_location(self):
        r=compile_source('int a = 1;\nprint(1 + );')
        self.assertFalse(r['success']); self.assertIn('línea 2',r['error'])
    def test_semantic_error_location(self):
        r=compile_source('int a = 1;\nprint(b);')
        self.assertFalse(r['success']); self.assertIn('línea 2',r['error'])
    def test_type_error(self):
        r=compile_source('string a = "hola"; int b = 2 + a;')
        self.assertFalse(r['success']); self.assertIn('Semántico',r['error'])
    def test_constant_optimization(self):
        r=self.compile_ok('int a = 2; int b = a * 3; print(b);',['6'],optimized=True)
        self.assertTrue(r['optimizations'])
    def test_dead_temporaries(self):
        r=self.compile_ok('int a = 2; int b = 3; print(a);',['2'],optimized=True)
        self.assertTrue(any('muerto' in n for n in r['optimizations']))
    def test_heap(self):
        r=self.compile_ok('int p = new(24); free(p); print(1);',['1'])
        self.assertEqual(r['cpu_heap_remaining'],{})
    def test_spill(self):
        r=self.compile_ok((Path(__file__).resolve().parents[1]/'examples/spill.clab').read_text(),['92'])
        self.assertGreater(r['spill_count'],0)
        self.assertIn('0x2000',r['cpu_ram'])
        self.assertTrue(any('ram' in t for t in r['cpu_trace']))
    def test_coverage_matrix(self): self.assertGreaterEqual(len(COVERAGE),18)
    def test_optimized_vs_unoptimized(self):
        source='int a = 2; int b = 5; print((a+b)*b);'
        self.assertEqual(self.compile_ok(source)['output'],self.compile_ok(source,optimized=True)['output'])

if __name__=='__main__': unittest.main()
