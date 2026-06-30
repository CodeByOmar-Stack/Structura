import unittest
from unittest.mock import patch

import main as main_module


class FakeApp:
    def run(self):
        raise KeyboardInterrupt


class MainTests(unittest.TestCase):
    def test_main_catches_keyboard_interrupt(self):
        with patch.object(main_module, "GestorCarpetasUI", return_value=FakeApp()):
            main_module.main()


if __name__ == "__main__":
    unittest.main()
