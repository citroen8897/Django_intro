from django.test import TestCase
from documents.models import Zip


class ZipTest(TestCase):

    def setUp(self):
        Zip.objects.create(
            title_zip='test',
            create_date_zip='2002-11-11', quantity_docs='22')
        Zip.objects.create(
            title_zip='test_2',
            create_date_zip='2012-24-03', quantity_docs='1')

    def test_zip_arg(self):
        zip_1 = Zip.objects.get(title_zip='test')
        zip_2 = Zip.objects.get(title_zip='test_2')
        self.assertEqual(
            zip_1.quantity_docs, "22")
        self.assertEqual(
            zip_2.quantity_docs, "1")
