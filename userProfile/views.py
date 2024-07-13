# views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from application.models import LicenseApplication
from .serializers import UserProfileSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retrieve the latest LicenseApplication for the authenticated user
        license_applications = LicenseApplication.objects.filter(applicant=self.request.user).order_by('-id')
        if license_applications.exists():
            return license_applications.first()
        return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
