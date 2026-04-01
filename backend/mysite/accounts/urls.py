from django.urls import path
from .views import CitizenSignup, LoginView

urlpatterns = [
    path('signup/', CitizenSignup.as_view(), name="citizen-signup"),
    path('login/', LoginView.as_view(), name="login"),
]