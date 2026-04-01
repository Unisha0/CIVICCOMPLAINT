from django.urls import path
from .views import CitizenSignup

urlpatterns = [

path('signup/', CitizenSignup.as_view()),
]