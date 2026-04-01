from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class CitizenSignup(APIView):
    permission_classes = []

    def post(self, request):
        fullname = request.data.get("fullname") or request.data.get("name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        password = request.data.get("password")

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        if not fullname or not password or not email:
            return Response({"error": "fullname, email and password required"}, status=400)

        User.objects.create_user(
            email=email,
            password=password,
            fullname=fullname,
            phone=phone,
            role="citizen"
        )

        return Response({"message": "Signup successful"}, status=201)


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if role and user.role != role:
                return Response({"error": f"User role mismatch. You are {user.role}"}, status=403)

            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "role": user.role,
                "fullname": user.fullname,
            })

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)