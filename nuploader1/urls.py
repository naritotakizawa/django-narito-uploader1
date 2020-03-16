from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'nuploader1'

router = DefaultRouter()
router.register(r'composites', views.CompositeViewSet, basename='composites')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/composites/get_composite_from_path/<path:request_path>', views.GetCompositeFromPath.as_view(), name='composites-frompath'),

    path('home/', views.top, name='top'),
    path('home/<path:request_path>', views.top, name='path'),
    path('zip/<int:pk>/', views.download_zip, name='download_zip'),
]
