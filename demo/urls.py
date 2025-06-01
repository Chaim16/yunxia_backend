from rest_framework.routers import DefaultRouter

from demo.view.user_view import UserViewSet

router = DefaultRouter()

urlpatterns = []
router.register(r'api/v1/user', UserViewSet, basename="user")

urlpatterns += router.urls
