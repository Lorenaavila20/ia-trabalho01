import unittest

class TestImports(unittest.TestCase):
    def test_main_importable(self):
        import src.main

if __name__ == "__main__":
    unittest.main()
