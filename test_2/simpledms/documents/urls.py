from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, ZipViewSet


router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='user')
router.register(r'zips', ZipViewSet, basename='user')
urlpatterns = router.urls
