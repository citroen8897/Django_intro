from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, ZipViewSet


router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'zips', ZipViewSet, basename='zip')
urlpatterns = router.urls
