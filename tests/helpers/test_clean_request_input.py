import cgi
import unittest

from src.masonite.helpers import clean_request_input


class TestCleanRequestInput(unittest.TestCase):

    def test_can_clean_string(self):
        self.assertEqual(clean_request_input('<img """><script>alert(\'hey\')</script>">'), '&lt;img &quot;&quot;&quot;&gt;&lt;script&gt;alert(&#x27;hey&#x27;)&lt;/script&gt;&quot;&gt;')

    def test_can_clean_list(self):
        self.assertEqual(clean_request_input(
            ['<img """><script>alert(\'hey\')</script>">', '<img """><script>alert(\'hey\')</script>">']
        ), [
            '&lt;img &quot;&quot;&quot;&gt;&lt;script&gt;alert(&#x27;hey&#x27;)&lt;/script&gt;&quot;&gt;',
            '&lt;img &quot;&quot;&quot;&gt;&lt;script&gt;alert(&#x27;hey&#x27;)&lt;/script&gt;&quot;&gt;'
        ])

    def test_can_clean_dictionary(self):
        self.assertEqual(clean_request_input(
            {'key': '<img """><script>alert(\'hey\')</script>">'}
        ), {'key': '&lt;img &quot;&quot;&quot;&gt;&lt;script&gt;alert(&#x27;hey&#x27;)&lt;/script&gt;&quot;&gt;'})

    def test_can_clean_multiple_dictionary(self):
        self.assertEqual(clean_request_input(
            {
                "conta_corrente": {
                    "ocultar": False,
                    "visao_geral": True,
                    "extrato": True
                }
            }
        ), {
            "conta_corrente": {
                "ocultar": False,
                "visao_geral": True,
                "extrato": True
            }
        })

    def test_does_not_clean_field_storage_objects(self):
        fieldstorage = FieldStorageTest()
        self.assertEqual(clean_request_input(fieldstorage), fieldstorage)

    def test_does_not_clean_bytes_objects(self):
        obj = b'test'
        self.assertEqual(clean_request_input(obj), obj)

    def test_does_not_clean_bytes_object_list(self):
        obj = [b'test', b'test']
        self.assertEqual(clean_request_input(obj), obj)

    def test_does_not_clean_bytes_objects_with_dicts(self):
        obj = {'x': b'test'}
        self.assertEqual(clean_request_input(obj), obj)

    def test_does_not_clean_quotes(self):
        obj = {'content': "awesome! 'i love you'"}
        self.assertEqual(clean_request_input(obj, quote=False)['content'], "awesome! 'i love you'")


class FieldStorageTest(cgi.FieldStorage):
    pass
