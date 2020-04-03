from collections import OrderedDict
from django.core.files.base import ContentFile
from django.http import Http404
from django.test import TestCase
from nuploader1.models import Composite
from nuploader1.serializers import CompositeSerializer, SimpleCompositeSerializer, SimpleCompositeRelation


class TestSimpleCompositeSerializer(TestCase):

    def test_output_data(self):
        composite = Composite.objects.create(name='django.txt', is_dir=False, parent=None, src=ContentFile(b'django', 'django.txt'))
        serializer = SimpleCompositeSerializer(instance=composite)
        self.assertDictEqual(
            serializer.data,
            {
                'pk': 1,
                'name': 'django.txt',
                'is_dir': False,
                'zip_depth': 0,
                'parent': None,
            }
        )


class TestCompositeSerializer(TestCase):

    def test_output_data(self):
        composite1 = Composite.objects.create(pk=1, name='hello', is_dir=True, parent=None, zip_depth=0)
        composite2 = Composite.objects.create(pk=2, name='depth1', is_dir=True, parent=composite1, zip_depth=1)
        composite3_1 = Composite.objects.create(pk=4, name='depth2.txt', is_dir=False, parent=composite2, src=ContentFile(b'depth2', 'depth2.txt'))
        composite3_2 = Composite.objects.create(pk=5, name='depth2', is_dir=True, parent=composite2)
        serializer = CompositeSerializer(instance=composite2)
        self.assertDictEqual(
            serializer.data,
            {
                'pk': 2,
                'name': 'depth1',
                'is_dir': True,
                'zip_depth': 1,
                'src': None,
                'parent': {'pk': 1, 'name': 'hello', 'is_dir': True, 'zip_depth': 0, 'parent': None},
                'composite_set':[
                    OrderedDict({'pk': 5, 'name': 'depth2', 'is_dir': True, 'zip_depth': 0, 'parent': 2}),
                    OrderedDict({'pk': 4, 'name': 'depth2.txt', 'is_dir': False, 'zip_depth': 0, 'parent': 2}),
                ]
            }
        )

    maxDiff = None
    def test_input_valid(self):
        input_data = {
            'name': 'hello',
            'is_dir': True,
            'zip_depth': 1,
            'parent': None,
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        input_data = {
            'name': 'python.txt',
            'is_dir': False,
            'parent': 1,
            'src': ContentFile(b'python', 'python.txt')
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_name_is_blank(self):
        input_data = {
            'name': '',
            'is_dir': False,
            'src': ContentFile(b'depth2', 'depth2.txt'),
            'zip_depth': 0,
            'parent': None,
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['name'][0]), 'この項目は空にできません。')

    def test_input_invalid_if_name_is_null(self):
        input_data = {
            'is_dir': False,
            'src': ContentFile(b'depth2', 'depth2.txt'),
            'zip_depth': 0,
            'parent': None,
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['name'][0]), 'この項目は必須です。')

    def test_input_invalid_if_parent_not_found(self):
        input_data = {
            'name': 'hello',
            'is_dir': True,
            'parent': 1,
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['parent'][0]), '主キー "1" は不正です - データが存在しません。',)

    def test_input_invalid_if_parent_is_file(self):
        input_data = {
            'name': 'hello.txt',
            'is_dir': False,
            'src': ContentFile(b'hello', 'hello.txt'),
            'parent': None,
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        input_data = {
            'name': 'hello',
            'is_dir': True,
            'parent': 1,
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['parent'][0]), '主キー "1" は不正です - データが存在しません。',)

    def test_input_invalid_if_parent_is_string(self):
        input_data = {
            'name': 'hello.txt',
            'is_dir': False,
            'src': ContentFile(b'hello', 'hello.txt'),
            'parent': None,
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        input_data = {
            'name': 'hello',
            'is_dir': True,
            'parent': 'test',
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['parent'][0]), '不正な型です。str 型ではなく主キーの値を入力してください。',)

    def test_input_invalid_if_parent_is_self(self):
        input_data = {
            'name': 'hello',
            'is_dir': True,
            'parent': None,
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        input_data = {
            'name': 'hello',
            'is_dir': True,
            'parent': 1,
        }
        serializer2 = CompositeSerializer(data=input_data, instance=serializer.instance)
        self.assertEqual(serializer2.is_valid(), False)
        self.assertEqual(str(serializer2.errors['non_field_errors'][0]), '親ディレクトリが自分です')

    def test_input_invalid_if_name_is_same(self):
        input_data = {
            'name': 'hello',
            'is_dir': True,
            'parent': None,
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        input_data = {
            'name': 'hello',
            'is_dir': True,
            'parent': None,
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), '同じ名前のファイル・ディレクトリが既に存在します')

    def test_input_invalid_if_no_file(self):
        input_data = {
            'name': 'hello.txt',
            'is_dir': False,
            'parent': None,
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), 'ファイルの時は、ファイルを添付してください')

    def test_input_invalid_if_empty_file(self):
        input_data = {
            'name': 'hello.txt',
            'is_dir': False,
            'src': None,
            'parent': None,
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), 'ファイルの時は、ファイルを添付してください')

    def test_input_invalid_if_change_no_file(self):
        input_data = {
            'name': 'hello',
            'is_dir': True,
            'src': None,
            'parent': None,
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), True)
        data = serializer.save()

        input_data = {
            'pk': 1,
            'name': 'hello',
            'is_dir': False,
            'parent': None,
        }
        serializer = CompositeSerializer(data=input_data, instance=data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), 'ファイルの時は、ファイルを添付してください')


    def test_input_invalid_if_dir_has_file(self):
        input_data = {
            'name': 'hello.txt',
            'is_dir': True,
            'src': ContentFile(b'hello', 'hello.txt'),
            'parent': None,
        }
        serializer = CompositeSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['non_field_errors'][0]), 'ディレクトリの時は、ファイルを添付しないでください')