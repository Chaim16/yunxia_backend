from rest_framework.routers import DefaultRouter

from user.view.user_view import UserViewSet

router = DefaultRouter()

urlpatterns = []
router.register(r'api/v1', UserViewSet, basename="user")

urlpatterns += router.urls
