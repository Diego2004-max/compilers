"""Pruebas de ejecución sobre un compilador y CPU reales (GCC/Clang)."""
import shutil
import unittest
from native_backend import build_native, find_compiler, NativeError


@unittest.skipUnless(find_compiler(), 'Se requiere GCC o Clang instalado')
class NativeBackendTests(unittest.TestCase):
    def test_expression(self):
        source = 'int a = 5; int b = 10; int c = 2; print(a + b * c);'
        self.assertEqual(build_native(source)['output'], '25\n')

    def test_stress(self):
        source = 'int a=3; int b=4; int c=5; int d=6; int e=7; int f=8; print((a+b)*(c+d)+(e+f));'
        self.assertEqual(build_native(source)['output'], '92\n')

    def test_types(self):
        source = 'float f=2.5; bool b=true; string s="hola"; print(f); print(b); print(s);'
        self.assertEqual(build_native(source)['output'], '2.5\ntrue\nhola\n')

    def test_error(self):
        with self.assertRaises(Exception):
            build_native('int a = ;')

    def test_no_fabricated_heap(self):
        with self.assertRaisesRegex(NativeError, 'new/free'):
            build_native('int p = new(8); print(p);')

@unittest.skipUnless(find_compiler(), 'Se requiere GCC o Clang instalado')
class NativeExtraTests(unittest.TestCase):
    def test_real_division(self):
        self.assertEqual(build_native('float x = 5 / 2; print(x);')['output'], '2.5\n')

    def test_string_comparison(self):
        self.assertEqual(build_native('string a = "hola"; string b = "hola"; print(a == b);')['output'], 'true\n')
