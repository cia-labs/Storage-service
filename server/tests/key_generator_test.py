import unittest
from unittest.mock import MagicMock, patch
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.join(current_dir, '..')  # Go up two levels to reach /Ciaos/server/
sys.path.append(parent_path)

from utils.key_generator import KeyGenerator

class KeyGeneratorTest(unittest.TestCase):
    @patch('utils.key_generator.get_latest_generated_key', return_value=42)
    def test_generate_key_thread_safe(self, mock_get_latest_generated_key):

        key_generator = KeyGenerator()

        import threading
        NUM_THREADS = 5
        threads = []
        for _ in range(NUM_THREADS):
            t = threading.Thread(target=key_generator.generate_key)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(key_generator.initial_value, 42)

        self.assertEqual(mock_get_latest_generated_key.call_count, 1)
        
        expected_counter = 42 + NUM_THREADS
        self.assertEqual(key_generator.counter, expected_counter)

    
    @patch('utils.key_generator.get_latest_generated_key', return_value=0)
    def test_initial_generate(self,mock_get_latest_generated_key):

        key_generator = KeyGenerator()
        
        key = key_generator.generate_key()
        
        expected_counter = 1
        self.assertTrue(type(key) is str)
        self.assertEqual(key_generator.counter, expected_counter)

    

