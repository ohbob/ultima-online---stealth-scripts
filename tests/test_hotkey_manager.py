import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hotkeysV4.hotkey_manager import HotkeyManager

class TestHotkeyManager(unittest.TestCase):

    def setUp(self):
        self.root = MagicMock()
        self.manager = HotkeyManager(self.root)

    def test_init(self):
        self.assertIsInstance(self.manager, HotkeyManager)
        self.assertEqual(self.manager.hotkeys_enabled, True)
        self.assertEqual(self.manager.auto_functions_enabled, False)

    def test_load_config(self):
        # Mock the open function to return a predefined config
        mock_config = {
            'hotkeys': {'test_func': 'ctrl+a'},
            'auto_functions': {'auto_test': {'enabled': True}},
            'auto_function_order': ['auto_test'],
            'friends': ['Friend1'],
            'pets': ['Pet1'],
            'activation_cooldown': 0.5
        }
        with patch('builtins.open', unittest.mock.mock_open(read_data=str(mock_config))):
            self.manager.load_config()

        self.assertEqual(self.manager.hotkeys, {'test_func': 'ctrl+a'})
        self.assertEqual(self.manager.auto_functions, {'auto_test': {'enabled': True}})
        self.assertEqual(self.manager.auto_function_order, ['auto_test'])
        self.assertEqual(self.manager.friends, ['Friend1'])
        self.assertEqual(self.manager.pets, ['Pet1'])
        self.assertEqual(self.manager.activation_cooldown, 0.5)

    def test_save_config(self):
        self.manager.hotkeys = {'test_func': 'ctrl+a'}
        self.manager.auto_functions = {'auto_test': {'enabled': True}}
        self.manager.auto_function_order = ['auto_test']
        self.manager.friends = ['Friend1']
        self.manager.pets = ['Pet1']
        self.manager.activation_cooldown = 0.5

        mock_open = unittest.mock.mock_open()
        with patch('builtins.open', mock_open):
            self.manager.save_config()

        mock_open.assert_called_once_with('hotkey_config.json', 'w')
        handle = mock_open()
        handle.write.assert_called_once()

    # Add more tests for other methods...

if __name__ == '__main__':
    unittest.main()