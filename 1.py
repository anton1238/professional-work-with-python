import json
import os
import unittest
import app

def update_date():
    current_path = str(os.path.dirname(os.path.abspath(__file__)))
    f_directories = os.path.join(current_path, 'fixtures/directories.json')
    f_documents = os.path.join(current_path, 'fixtures/documents.json')
    with open(f_documents, 'r') as out_docs:
        documents = json.load(out_docs)
    with open(f_directories, 'r') as out_dirs:
        directories = json.load(out_dirs)
    return directories, documents

class TestSecretaryProgram(unittest.TestCase):

    def setUp(self):
        print('method setUp')

    def tearDown(self):
        print('method tearDown')

    def test_get_doc_owner_name(self):
        self.assertEqual(app.get_doc_owner_name('2207 876234'), 'Василий Гупкин')

    def test_add_new_doc(self):
        self.assertEqual(app.add_new_doc('7311', 'pass', 'Shamil', 2), 2)

    def test_delete_doc(self):
        self.assertTrue(app.delete_doc('10006'))

if __name__ == '__main__':
    unittest.main()