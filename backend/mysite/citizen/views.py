from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()


class CitizenSignup(APIView):

    def post(self, request):

        fullname = request.data.get("fullname") or request.data.get("name")

        email = request.data.get("email")

        phone = request.data.get("phone")

        password = request.data.get("password")

        if User.objects.filter(email=email).exists():

            return Response({"error": "Email already exists"}, status=400)

        if not fullname:
            return Response({"error": "fullname required"})
        User.objects.create_user(

            email=email,

            password=password,

            fullname=fullname,

            phone=phone,

            role="citizen"
        )

        return Response({"message": "Signup successful"})