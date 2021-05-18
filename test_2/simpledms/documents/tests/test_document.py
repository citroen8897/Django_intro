from django.test import TestCase
from documents.models import Document


class DocumentTest(TestCase):

    def setUp(self):
        Document.objects.create(
            title='test', main_file='test.py', reg_number='001_001',
            create_date='2002-11-11', comment='test')
        Document.objects.create(
            title='test_2', main_file='test_2.py', reg_number='002_002',
            create_date='2003-01-13', comment='test_2')

    def test_doc_arg(self):
        doc_1 = Document.objects.get(title='test')
        doc_2 = Document.objects.get(title='test_2')
        self.assertEqual(
            doc_1.reg_number, "001_001")
        self.assertEqual(
            doc_2.comment, "test_2")
