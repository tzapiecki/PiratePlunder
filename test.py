from server_classes import server_utilities
import unittest

class TestIsRoomCodeValid(unittest.TestCase):

    def test_simple_valid_codes(self):
        self.assertTrue(server_utilities.is_room_code_valid("ABC"))
        self.assertTrue(server_utilities.is_room_code_valid("abc"))
        self.assertTrue(server_utilities.is_room_code_valid("123"))
        self.assertTrue(server_utilities.is_room_code_valid("a"))
        self.assertTrue(server_utilities.is_room_code_valid("abcABC123"))

if __name__ == '__main__':
    unittest.main()