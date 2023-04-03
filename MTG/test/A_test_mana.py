# mana payment
import mock
import unittest
from collections import defaultdict

from MTG import mana
from MTG import player

class TestManaPayment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = mana.ManaPool()
        cls.m.controller = player.Player([])

    def test_mana_pool(self):
        with mock.patch('builtins.input', return_value=''):
            self.assertFalse(self.m.canPay('1'))
            self.m.add('W', 0)
            self.m.add('U', 0)
            self.m.add('B', 0)
            self.m.add('R', 0)
            self.m.add('G', 0)
            self.m.add('C', 0)
            self.m.clear()
            self.m.add('1', 13)
            print(self.m.pool)
            # c = self.m.canPay('7')
            # self.m.pay(c)
            self.assertTrue(self.m.canPay('7'))
            # print(self.m.pool)
            self.m.clear()
            self.m.clear()
            self.assertFalse(self.m.canPay('1'))

    def test_basic_mana_payment(self):
        self.assertEqual(self.m.canPay('U')[mana.Mana.BLUE], 1)
        c = self.m.canPay('UUW')
        self.assertEqual(c[mana.Mana.BLUE], 2)
        self.assertEqual(c[mana.Mana.WHITE], 1)

    def test_numbers_in_mana_costs(self):
        with mock.patch('builtins.input', return_value=''):
            self.assertEqual(type(self.m.canPay('4U')), defaultdict)
            self.assertTrue(self.m.canPay('7'))
            self.assertTrue(self.m.canPay('0'))
            self.assertFalse(self.m.canPay('1R'))

        with mock.patch('builtins.input', side_effect=['RUUW']):
            self.assertFalse(self.m.canPay('4U'))

    def test_hybrid_mana_costs(self):
        with mock.patch('builtins.input', side_effect=['0', '0', '0', '']):
            c = self.m.canPay('(2/R)(2/W)(2/U)')
            self.assertEqual(c[mana.Mana.BLUE] + c[mana.Mana.WHITE], 6)

        with mock.patch('builtins.input', side_effect=['1', '0', '1', '']):
            self.assertFalse(self.m.canPay('(U/R)(2/W)(2/U)'))

        with mock.patch('builtins.input', side_effect=['0', '1', '1', 'UU']):
            c = self.m.canPay('U(2/R)(G/W)(W/U)')
            self.assertEqual(c[mana.Mana.BLUE], 4)
            self.assertEqual(c[mana.Mana.WHITE], 1)

if __name__ == '__main__':
    unittest.main()
