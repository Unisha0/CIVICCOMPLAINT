from rest_framework import serializers
from .models import Complaint
from django.contrib.auth import get_user_model

User = get_user_model()  # your custom user model if any

# Nested user serializer
class CitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fullname', 'email', 'phone']  # add 'location' if needed

# Complaint serializer with nested citizen info
class ComplaintSerializer(serializers.ModelSerializer):
    citizen = CitizenSerializer(read_only=True)  # use nested serializer

    class Meta:
        model = Complaint
        fields = "__all__"
        read_only_fields = ['id', 'created_at']