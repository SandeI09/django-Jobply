from django.urls import path
from . import views


urlpatterns = [
    path("user-register/", views.UserRegisterView.as_view(), name="user_register"),
    path("user-login/", views.UserLoginView.as_view(), name="user_login"),
    path("user-logout/", views.userLogout, name="user_logout"),
    path("activate/<str:username>/<str:key>/", views.UserAccountActivationView.as_view(), name="ac_activation"),
    path("resend-activation/<int:id>/", views.ResendEmailActivaiton.as_view(), name="resend_ac_activation"),
    path("user_profile/<int:pk>/", views.UserProfileView.as_view(), name="user_profile"),
    path("user_profile/update/<int:pk>/", views.UpdateUserProfileView.as_view(), name="user_profile_update"),
]
