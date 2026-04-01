from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, generics, status
from rest_framework.renderers import JSONRenderer
import json

from .models import Complaint
from .serializers import ComplaintSerializer
from .classifier import classify_complaint

# ✅ UTF-8 JSON Renderer
class UTF8JSONRenderer(JSONRenderer):
    charset = 'utf-8'
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b''
        return json.dumps(data, ensure_ascii=False, indent=None).encode('utf-8')


# ===============================
# 🔐 FULL CRUD (LOGIN REQUIRED)
# ===============================
class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all().order_by("-created_at")
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UTF8JSONRenderer]

    def perform_create(self, serializer):
        user = self.request.user
        description = serializer.validated_data.get("description", "")
        result = classify_complaint(description)

        # Save complaint with full citizen info
        serializer.save(
            citizen=user,
            citizen_name=user.fullname,
            citizen_email=user.email,
            citizen_phone=user.phone,
            citizen_location=user.location,
            category=result.get("category", "unknown"),
            authority=result.get("authority", "General Authority"),
            confidence=result.get("confidence", 0.0),
            ml_status=result.get("status", "UNCERTAIN"),
            status="PENDING",
            language=result.get("language", "en")
        )


# ===============================
# 🚀 SUBMIT COMPLAINT (AI + CLEAN)
# ===============================
class SubmitComplaint(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UTF8JSONRenderer]

    VALID_CATEGORIES = ["water", "road", "electricity", "garbage"]

    def post(self, request):
        data = request.data.copy()
        description = data.get("description", "").strip()

        # ✅ Get lat/lng from frontend
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not description:
            return Response({"error": "Description is required"}, status=400)

        if not latitude or not longitude:
            return Response({"error": "Location (latitude & longitude) is required"}, status=400)

        user = request.user

        try:
            result = classify_complaint(description)
            category = result.get("category", "").strip().lower()

            if category not in self.VALID_CATEGORIES:
                category = "unknown"

            data.update({
                "category": category,
                "authority": result.get("authority", "General Authority"),
                "confidence": result.get("confidence", 0.0),
                "ml_status": result.get("status", "UNCERTAIN"),
                "status": "PENDING",
                "language": result.get("language", "en"),
            })

        except Exception:
            data.update({
                "category": "unknown",
                "authority": "General Authority",
                "confidence": 0.0,
                "ml_status": "ERROR",
                "status": "PENDING",
                "language": "unknown",
            })

        # ✅ Add user + location
        data.update({
            "citizen": user.id,
            "latitude": latitude,
            "longitude": longitude
        })

        serializer = ComplaintSerializer(data=data)

        if serializer.is_valid():
            complaint = serializer.save(citizen=user)

            return Response({
                "message": "Complaint submitted successfully",
                "data": {
                    "id": complaint.id,
                    "category": complaint.category,
                    "authority": complaint.authority,
                    "ml_status": complaint.ml_status,
                    "confidence": complaint.confidence,
                    "status": complaint.status,
                    "latitude": complaint.latitude,
                    "longitude": complaint.longitude
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ===============================
# 🏛️ AUTHORITY CATEGORY FILTER
# ===============================
class AuthorityComplaints(generics.ListAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UTF8JSONRenderer]

    def get_queryset(self):
        category = self.kwargs.get("category", "").strip().lower()
        VALID_CATEGORIES = ["water", "road", "electricity", "garbage"]
        if category in VALID_CATEGORIES:
            return Complaint.objects.filter(category__iexact=category).order_by("-created_at")
        return Complaint.objects.none()


# ===============================
# 🔄 UPDATE STATUS (AUTHORITY USE)
# ===============================
class UpdateComplaintStatus(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UTF8JSONRenderer]

    def patch(self, request, pk):
        try:
            complaint = Complaint.objects.get(pk=pk)
        except Complaint.DoesNotExist:
            return Response({"error": "Complaint not found"}, status=404)

        new_status = request.data.get("status")
        VALID_STATUS = ["PENDING", "ACCEPTED", "REJECTED", "RESOLVED"]

        if new_status not in VALID_STATUS:
            return Response({"error": "Invalid status"}, status=400)

        complaint.status = new_status
        complaint.save()

        return Response({"message": "Status updated successfully", "status": complaint.status})