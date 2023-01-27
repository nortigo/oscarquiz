from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterViewSet, AuthenticatedUserView

app_name = 'account__api'


router = routers.SimpleRouter()
router.register('register', RegisterViewSet, basename='register')

urlpatterns = router.urls

urlpatterns += [
    path('me/', AuthenticatedUserView.as_view(), name='me'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
