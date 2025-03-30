from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from user.views import CreateUserView

app_name = "user"

urlpatterns = [
    # path("register/", CreateUserView.as_view(), name="create"),
    # # path("login/", CreateTokenView.as_view(), name="login"),
    # path("me/", ManageUserView.as_view(), name="manage"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", CreateUserView.as_view(), name="create_user"),
]
