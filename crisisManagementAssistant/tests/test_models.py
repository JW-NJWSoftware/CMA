from django.test import TestCase
from CMAfile.models import CMDoc


class CMDocModelTest(TestCase):
    def test_default_text(self):
        file_ = CMDoc()
        self.assertEqual(file_.name, '')

    def test_list_ordering(self):
        file1 = CMDoc.objects.create(name='f1')
        file2 = CMDoc.objects.create(name='f2')
        file3 = CMDoc.objects.create(name='f3')
        self.assertEqual(
            list(CMDoc.objects.all()),
            [file1, file2, file3]
        )
