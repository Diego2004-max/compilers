import unittest
from compiler import compile_source

class RegressionTests(unittest.TestCase):
    def test_chain_of_constant_propagation(self):
        result = compile_source('int a = 2; int b = a; int c = b + 3; print(c);', optimized=True)
        self.assertTrue(result['success'], result.get('error'))
        self.assertEqual(result['output'], ['5'])
    def test_scope_redeclaration_rejected(self):
        result = compile_source('int x = 1; int x = 2;')
        self.assertFalse(result['success'])
        self.assertIn('duplicada', result['error'])
    def test_unknown_function_rejected(self):
        result = compile_source('desconocida();')
        self.assertFalse(result['success'])
        self.assertIn('Función', result['error'])
    def test_register_count_invalid(self):
        result = compile_source('int x = 2;', registers=2)
        self.assertFalse(result['success'])
        self.assertIn('3 registros', result['error'])
