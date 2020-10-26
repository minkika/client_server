import io
import unittest
from unittest import mock

from common.utils import Message, PresenceMessage, Response
from common.variables import DICT_ANSWER_CODE, PRESENCE


class TestMessages(unittest.TestCase):

    def test_creation(self):
        message = Message(PRESENCE, 1)
        self.assertEqual(message.time, 1)

    def test_representation(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            message = Message(PRESENCE)
            print(message)
        assert fake_stdout.getvalue() == 'message >>> presence\n'

    def test_to_bytes(self):
        message = Message(PRESENCE, 1)
        self.assertIsInstance(message.to_bytes(), bytes)

    def test_serialize(self):
        message = Message(PRESENCE, 1)
        self.assertIn('time', message.serialize().keys())

    def test_presence_message(self):
        message = PresenceMessage()
        self.assertIsNone(message.user)
        self.assertEqual(message.action, PRESENCE)
        self.assertListEqual([*message.serialize().keys()], ['action', 'time', 'user'])


class TestResponses(unittest.TestCase):
    def test_codes(self):
        for code in DICT_ANSWER_CODE.keys():
            with self.subTest(i=code):
                response = Response(code)
                self.assertEqual(response.get_code(), code, f'Код не распознан для {code}')
                self.assertIsInstance(response.to_bytes(), bytes)
                self.assertIsInstance(response.get_message(), str)
                self.assertEqual(response.get_message(), f'{DICT_ANSWER_CODE[code]}')


if __name__ == '__main__':
    unittest.main()
