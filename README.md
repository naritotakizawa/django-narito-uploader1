# nuploader1

Django REST frameworkとVueで作ったファイルアップローダー

## インストールと動かし方

### すぐに動かしたり、コードに手を入れてみたい

リポジトリにサンプルプロジェクトを同封しているので、それを使って動かしたりできます。

```
git clone https://github.com/naritotakizawa/django-narito-uploader1
cd django-narito-blog2
pipenv install
pipenv shell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

データの削除や追加、更新は、ログイン必須です。先にログインをしておきましょう。

`http://127.0.0.1:8000/uploader/home/`にアクセスすると、ページが表示され操作できます。

### 既にあるDjangoプロジェクトに導入したい

```
pip install https://github.com/naritotakizawa/django-narito-uploader1/archive/master.tar.gz
```

`settings.py`に追加する。

```python
INSTALLED_APPS = [
    'nuploader1.apps.Nuploader1Config',  # これ
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework'  # これ
]
```

メディアファイルの設定例

```python
# アップロードファイルの設定
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

`urls.py`の設定例

```python
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('uploader/', include('nuploader1.urls')),
]


# 開発環境でのメディアファイルの配信設定
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
```


マイグレート、スーパーユーザー作成、開発用サーバーの起動。

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

データの削除や追加、更新は、ログイン必須です。先にログインをしておきましょう。

`http://127.0.0.1:8000/uploader/home/`にアクセスすると、ページが表示され操作できます。