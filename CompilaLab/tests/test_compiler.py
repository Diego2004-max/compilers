import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from compiler import compile_source

EXAMPLES=Path(__file__).resolve().parents[1]/'examples'
class CompilerTests(unittest.TestCase):
    def example(self,name,**opts): return compile_source((EXAMPLES/name).read_text(encoding='utf-8'),**opts)
    def test_correct(self):
        r=self.example('correcto.clab'); self.assertTrue(r['success'],r['error']); self.assertEqual(r['output'],['25'])
    def test_spill(self):
        r=self.example('spill.clab'); self.assertTrue(r['success'],r['error']); self.assertGreater(r['spill_count'],0); self.assertEqual(r['output'],['92'])
    def test_optimization(self):
        r=self.example('spill.clab',optimized=True); self.assertTrue(r['success'],r['error']); self.assertEqual(r['output'],['92']); self.assertTrue(r['optimizations'])
    def test_semantic(self):
        r=self.example('error_semantico.clab'); self.assertFalse(r['success']); self.assertIn('Semántico',r['error'])
    def test_memory(self):
        r=self.example('memoria.clab'); self.assertTrue(r['success'],r['error']); self.assertEqual(r['output'],['500']); self.assertIn('HEAP FREE', ' '.join(r['memory_events']))
    def test_lexical(self):
        r=compile_source('int x = 2 @ 3;'); self.assertFalse(r['success']); self.assertIn('Léxico',r['error'])
    def test_syntax(self):
        r=compile_source('int x = (2 + );'); self.assertFalse(r['success']); self.assertIn('Sintáctico',r['error'])
    def test_undefined(self):
        r=compile_source('int x = z + 1;'); self.assertFalse(r['success']); self.assertIn('Semántico',r['error'])
    def test_divzero(self):
        r=compile_source('int x = 1 / 0;'); self.assertFalse(r['success']); self.assertIn('Semántico',r['error'])
    def test_double_free(self):
        r=compile_source('int p = new(12); free(p); free(p);'); self.assertFalse(r['success']); self.assertIn('Doble free',r['error'])
if __name__=='__main__': unittest.main()
