from django.test import TestCase
from nuploader1.models import Composite


class TestComposite(TestCase):

    def test_str_if_dir(self):
        composite = Composite.objects.create(name='hello', is_dir=True)
        self.assertEqual(str(composite), '1 - hello/')

    def test_str_if_file(self):
        composite = Composite.objects.create(name='hello', is_dir=False)
        self.assertEqual(str(composite), '1 - hello')

    def test_get_display_name_if_dir(self):
        composite = Composite.objects.create(name='hello', is_dir=True)
        self.assertEqual(composite.get_display_name(), 'hello/')

    def test_get_display_name_if_file(self):
        composite = Composite.objects.create(name='hello', is_dir=False)
        self.assertEqual(composite.get_display_name(), 'hello')
