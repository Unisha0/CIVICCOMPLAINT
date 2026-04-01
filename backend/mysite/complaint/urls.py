from django.urls import path
from .views import SubmitComplaint, AuthorityComplaints

urlpatterns = [
    path("submit/", SubmitComplaint.as_view(), name="submit-complaint"),
    path("authority/<str:category>/", AuthorityComplaints.as_view(), name="authority-complaints"),
]