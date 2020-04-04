import io
import zipfile
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from nuploader1.models import Composite


class TestCompositeViewSet(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            username='user',
            email='a@a.com',
            password='password',
        )

    def test_list_composite(self):
        composite1 = Composite.objects.create(pk=1, name='1', is_dir=True, parent=None)
        composite2 = Composite.objects.create(pk=2, name='2', is_dir=True, parent=composite1)
        composite3 = Composite.objects.create(pk=3, name='3', is_dir=True, parent=composite2)
        response = self.client.get(resolve_url('nuploader1:composites-list'))
        self.assertEqual(Composite.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(
            response.content,
            [
                {
                    'pk': 1, 'name': '1', 'is_dir': True, 'parent': None, 'src': None, 'zip_depth': 0,
                    'composite_set': [{'pk': 2, 'name': '2', 'is_dir': True, 'zip_depth': 0, 'parent': 1}]
                }
            ]
        )

    def test_create_composite_success(self):
        self.client.login(username='user', password='password')
        data = {
            'name': 'test',
            'is_dir': True,
        }
        response = self.client.post(resolve_url('nuploader1:composites-list'), data, format='json')

        self.assertEqual(Composite.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(
            response.content,
            {
                'pk': 1,
                'name': 'test',
                'is_dir': True,
                'src': None,
                'parent': None,
                'zip_depth': 0,
                'composite_set': [],
            }
        )

    def test_create_composite_failure(self):
        self.client.login(username='user', password='password')
        data = {
            'is_dir': True,
        }
        response = self.client.post(resolve_url('nuploader1:composites-list'), data, format='json')

        self.assertEqual(Composite.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(
            response.content,
            {'name': ['この項目は必須です。']}
        )

    def test_create_composite_no_login(self):
        data = {
            'name': 'test',
            'is_dir': True,
        }
        response = self.client.post(resolve_url('nuploader1:composites-list'), data, format='json')
        self.assertEqual(Composite.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(
            response.content,
            {'detail': '認証情報が含まれていません。'}
        )

    def test_update_composite_success(self):
        self.client.login(username='user', password='password')
        composite1 = Composite.objects.create(name='hello', parent=None, is_dir=True, zip_depth=5)
        data = {
            'name': 'world',
        }
        response = self.client.patch(resolve_url('nuploader1:composites-detail', pk=1), data, format='json')
        self.assertEqual(Composite.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(
            response.content,
            {
                'pk': 1,
                'name': 'world',
                'is_dir': True,
                'src': None,
                'parent': None,
                'zip_depth': 5,
                'composite_set': [],
            }
        )

    def test_update_composite_failure(self):
        self.client.login(username='user', password='password')
        composite1 = Composite.objects.create(name='hello', parent=None, is_dir=True, zip_depth=5)
        data = {
            'is_dir': False,
        }
        response = self.client.patch(resolve_url('nuploader1:composites-detail', pk=1), data, format='json')
        self.assertEqual(Composite.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(
            response.content,
            {'non_field_errors': ['ファイルの時は、ファイルを添付してください']}
        )

    def test_update_composite_no_login(self):
        composite1 = Composite.objects.create(name='hello', parent=None, is_dir=True, zip_depth=5)
        data = {
            'name': 'world',
        }
        response = self.client.patch(resolve_url('nuploader1:composites-detail', pk=1), data, format='json')
        self.assertEqual(Composite.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(
            response.content,
            {'detail': '認証情報が含まれていません。'}
        )

    def test_delete_composite_success(self):
        self.client.login(username='user', password='password')
        composite1 = Composite.objects.create(name='hello', parent=None, is_dir=True, zip_depth=5)
        response = self.client.delete(resolve_url('nuploader1:composites-detail', pk=1))
        self.assertEqual(Composite.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b'')

    def test_delete_composite_failure(self):
        self.client.login(username='user', password='password')
        composite1 = Composite.objects.create(name='hello', parent=None, is_dir=True, zip_depth=5)
        response = self.client.delete(resolve_url('nuploader1:composites-detail', pk=2))
        self.assertEqual(Composite.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertJSONEqual(response.content, {"detail": "見つかりませんでした。"})

    def test_delete_composite_no_login(self):
        composite1 = Composite.objects.create(name='hello', parent=None, is_dir=True, zip_depth=5)
        response = self.client.delete(resolve_url('nuploader1:composites-detail', pk=1))
        self.assertEqual(Composite.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(
            response.content,
            {'detail': '認証情報が含まれていません。'}
        )


class TestGetCompositeFromPath(APITestCase):

    def test_get_success(self):
        composite1 = Composite.objects.create(pk=1, name='hello', is_dir=True, parent=None)
        composite2 = Composite.objects.create(pk=2, name='world', is_dir=True, parent=composite1)
        composite3 = Composite.objects.create(pk=3, name='django', is_dir=True, parent=composite2)
        response = self.client.get(resolve_url('nuploader1:composites_frompath', request_path='/hello/world/django/'))
        self.assertEqual(Composite.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(
            response.content,
            {
                'composite_set': [],
                'is_dir': True,
                'name': 'django',
                'parent': {'is_dir': True, 'name': 'world', 'pk': 2, 'zip_depth': 0, 'parent': 1},
                'pk': 3,
                'src': None,
                'zip_depth': 0}
        )

    def test_get_failure(self):
        composite1 = Composite.objects.create(pk=1, name='hello', is_dir=True, parent=None)
        response = self.client.get(resolve_url('nuploader1:composites_frompath', request_path='/aaaa/'))
        self.assertEqual(Composite.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertJSONEqual(response.content, {"detail": "見つかりませんでした。"})


class TestTop(TestCase):

    def test_get_success(self):
        response = self.client.get(resolve_url('nuploader1:serve'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'N Uploader1')

    def test_get_dir(self):
        composite1 = Composite.objects.create(pk=1, name='hello', is_dir=True, parent=None)
        response = self.client.get(resolve_url('nuploader1:path', request_path='/hello/'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'N Uploader1')

    def test_get_dir2(self):
        """存在しないパスでも、ディレクトリっぽければ200でhtmlを返す"""
        composite1 = Composite.objects.create(pk=1, name='hello', is_dir=True, parent=None)
        response = self.client.get(resolve_url('nuploader1:path', request_path='/aaaaaaaaaaaaa/'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_file(self):
        composite1 = Composite.objects.create(pk=1, name='hello.txt', is_dir=False, parent=None, src=ContentFile(b'hello', 'hello.txt'))
        response = self.client.get(resolve_url('nuploader1:path', request_path='/hello.txt'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.streaming_content), [b'hello'])



class TestZip(TestCase):

    def test_get_success(self):
        composite1 = Composite.objects.create(pk=1, name='hello', is_dir=True, parent=None, zip_depth=2)

        # zip_depthが1
        composite2_1 = Composite.objects.create(pk=2, name='depth1', is_dir=True, parent=composite1)
        composite2_2 = Composite.objects.create(pk=3, name='depth1.txt', is_dir=False, parent=composite1, src=ContentFile(b'depth1', 'depth1.txt'))

        # zip_depthが2
        composite3_1 = Composite.objects.create(pk=4, name='depth2.txt', is_dir=False, parent=composite2_1, src=ContentFile(b'depth2', 'depth2.txt'))
        composite3_2 = Composite.objects.create(pk=5, name='depth2', is_dir=True, parent=composite2_1)

        # zip_depthが3(今回は含めない)
        composite4 = Composite.objects.create(pk=6, name='depth3.txt', is_dir=False, parent=composite3_2,src=ContentFile(b'depth3', 'depth3.txt'))

        response = self.client.get(resolve_url('nuploader1:download_zip', pk=composite1.pk))
        f = io.BytesIO(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(zipfile.ZipFile(f).namelist(), ['depth1.txt', 'depth1/depth2.txt'])

    def test_get_failure1(self):
        composite1 = Composite.objects.create(pk=1, name='hello', is_dir=True, parent=None, zip_depth=0)
        composite2 = Composite.objects.create(pk=2, name='depth1.txt', is_dir=False, parent=composite1, src=ContentFile(b'depth1', 'depth1.txt'))
        response = self.client.get(resolve_url('nuploader1:download_zip', pk=composite1.pk))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_failure2(self):
        composite1 = Composite.objects.create(pk=1, name='depth1.txt', is_dir=False, parent=None, src=ContentFile(b'depth1', 'depth1.txt'))
        response = self.client.get(resolve_url('nuploader1:download_zip', pk=composite1.pk))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
