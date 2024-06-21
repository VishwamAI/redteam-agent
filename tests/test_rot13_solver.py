import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rot13_solver import rot13_decrypt

class TestRot13Solver(unittest.TestCase):
    def test_rot13_decrypt(self):
        # Test with a simple message
        self.assertEqual(rot13_decrypt("uryyb"), "hello")

        # Test with a message containing uppercase letters
        self.assertEqual(rot13_decrypt("URYYB"), "HELLO")

        # Test with a message containing mixed case letters
        self.assertEqual(rot13_decrypt("Uryyb"), "Hello")

        # Test with a message containing non-alphabetic characters
        self.assertEqual(rot13_decrypt("uryyb123!"), "hello123!")

        # Test with an empty string
        self.assertEqual(rot13_decrypt(""), "")

        # Test with the provided encoded message
        self.assertEqual(rot13_decrypt("cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_uJdSftmh}"), "picoCTF{next_time_I'll_try_2_rounds_of_rot13_hWqFsgzu}")

if __name__ == "__main__":
    unittest.main()
