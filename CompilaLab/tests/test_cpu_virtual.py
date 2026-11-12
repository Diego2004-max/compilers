import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compiler import compile_source

EXAMPLES = Path(__file__).resolve().parents[1] / 'examples'

class VirtualCPUTests(unittest.TestCase):
    def check(self, source, expected, optimized=False, registers=3):
        result = compile_source(source, registers=registers, optimized=optimized)
        self.assertTrue(result['success'], result['error'])
        self.assertEqual(result['output'], expected)
        self.assertEqual(result['cpu_output'], expected)
        self.assertTrue(result['cpu_matches_tac'])
        return result

    def test_spill_cpu_ram(self):
        r = self.check((EXAMPLES/'spill.clab').read_text(), ['92'])
        self.assertEqual(r['spill_count'], 7)
        self.assertGreaterEqual(len(r['cpu_ram']), 7)
        self.assertIn('0x2000', r['cpu_ram'])
        self.assertTrue(any('STORE' in step['instruction'] for step in r['cpu_trace']))
        self.assertTrue(any('LOAD' in step['instruction'] for step in r['cpu_trace']))

    def test_spill_optimized(self):
        self.check((EXAMPLES/'spill.clab').read_text(), ['92'], optimized=True)

    def test_arithmetic(self):
        self.check('int a = 3; int b = 8; int c = (a + b) * 2 - 1; print(c);', ['21'])

    def test_memory_and_call(self):
        r = self.check((EXAMPLES/'memoria.clab').read_text(), ['500'])
        self.assertEqual(r['cpu_heap_remaining'], {})
        self.assertIn('HEAP FREE', ' '.join(r['cpu_memory_events']))
        self.assertTrue(any('CALL-SAVE' in event for event in r['register_events']))

    def test_multiple_prints(self):
        self.check('int a = 10; print(a); a = a + 1; print(a);', ['10','11'])

    def test_comparison(self):
        self.check('bool a = 3 < 4; print(a);', ['True'])

if __name__ == '__main__': unittest.main()
