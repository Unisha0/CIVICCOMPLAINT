from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Complaint(models.Model):
    citizen = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    language = models.CharField(max_length=10, blank=True)
    category = models.CharField(max_length=50, blank=True)
    authority = models.CharField(max_length=100, blank=True)
    confidence = models.FloatField(default=0.0)
    ml_status = models.CharField(max_length=20, default="UNCERTAIN")
    status = models.CharField(max_length=20, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} {self.category} {self.status}"


class ElectricityComplaint(Complaint):
    class Meta:
        proxy = True
        verbose_name_plural = "Electricity Complaints"


class RoadComplaint(Complaint):
    class Meta:
        proxy = True
        verbose_name_plural = "Road Complaints"


class GarbageComplaint(Complaint):
    class Meta:
        proxy = True
        verbose_name_plural = "Garbage Complaints"


class WaterComplaint(Complaint):
    class Meta:
        proxy = True
        verbose_name_plural = "Water Complaints"