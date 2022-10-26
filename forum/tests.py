from django.test import TestCase
from .templatetags.cut_number import cut_number


class CutNumberTest(TestCase):
    def test_thousand(self):
        value = cut_number(4000)
        self.assertEqual(value, '4k')

    def test_million(self):
        value = cut_number(5400000)
        self.assertEqual(value, '54m')
