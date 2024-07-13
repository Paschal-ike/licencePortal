from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import LicenseApplication
from .serializers import LicenseApplicationSerializer, RenewalApplicationSerializer,ReissueApplicationSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser

class BaseLicenseApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def handle_no_permission(self):
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

class NewApplicationCreateView(BaseLicenseApplicationView):
    """
    Create a new license application.
    """
    parser_classes = [MultiPartParser]
    
    @swagger_auto_schema(
        request_body=LicenseApplicationSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Created",
                schema=LicenseApplicationSerializer()
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        },
        operation_description="Create a new license application."
    )
    def post(self, request, *args, **kwargs):
        serializer = LicenseApplicationSerializer(data=request.data)
        if serializer.is_valid():
            # Save application with authenticated user
            new_application = serializer.save(applicant=request.user)
            
            # Prepare response data
            response_data = serializer.data
            response_data['applicant'] = {
                'id': request.user.id,
                'username': request.user.username,
                # 'first_name': request.user.first_name,
                # 'last_name': request.user.last_name,
                'email': request.user.email,
                # 'phone_number': request.user.phone_number,
            }
            response_data['appointment_location'] = new_application.appointment_location
            response_data['appointment_day'] = new_application.appointment_day
            response_data['appointment_date'] = new_application.appointment_date
            response_data['appointment_time'] = new_application.appointment_time
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RenewalApplicationCreateView(APIView):
    """
    Create a renewal license application.
    """
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['licence_id'],
            properties={
                'licence_id': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="User and appointment information retrieved",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'appointment_location': openapi.Schema(type=openapi.TYPE_STRING),
                        'appointment_day': openapi.Schema(type=openapi.TYPE_STRING),
                        'appointment_date': openapi.Schema(type=openapi.TYPE_STRING),
                        'appointment_time': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="User not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
        },
        operation_description="Retrieve user and appointment information for license renewal using the license ID."
    )
    def post(self, request):
        
        print("Request data:", request.data)  # Debug print
        licence_id = request.data.get('licence_id')
        print("Extracted licence_id:", licence_id)  # Debug print
        
        if licence_id is None:
            return Response({"detail": "licence_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = LicenseApplication.objects.filter(licence_id=licence_id).first()
        
        if user:
            renewal_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'appointment_location': user.appointment_location,
                'appointment_day': user.appointment_day,
                'appointment_date': user.appointment_date,
                'appointment_time': user.appointment_time,
            }
            return Response(renewal_data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": f"User not found for the provided license ID: {licence_id}"}, status=status.HTTP_404_NOT_FOUND)


class ReissueApplicationCreateView(APIView):
    """
    Create a reissue license application.
    """
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        request_body=ReissueApplicationSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Reissue Application Created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'appointment_location': openapi.Schema(type=openapi.TYPE_STRING),
                        'appointment_day': openapi.Schema(type=openapi.TYPE_STRING),
                        'appointment_date': openapi.Schema(type=openapi.TYPE_STRING),
                        'appointment_time': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="User details not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'licence_id': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                        'affidavit_police_report': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
                    }
                )
            ),
        },
        operation_description="Create a reissue license application with license number and affidavit/police report."
    )
    def post(self, request, *args, **kwargs):
        serializer = ReissueApplicationSerializer(data=request.data)
        if serializer.is_valid():
            licence_id = serializer.validated_data.get('licence_id')
            affidavit_police_report = serializer.validated_data.get('affidavit_police_report')
            
            try:
                # Find the existing license application
                existing_application = LicenseApplication.objects.get(licence_id=licence_id)
                
                # Create reissue application
                reissue_application = LicenseApplication.objects.create(
                    licence_id=licence_id,
                    first_name=existing_application.first_name,
                    last_name=existing_application.last_name,
                    date_of_birth=existing_application.date_of_birth,
                    affidavit_police_report=affidavit_police_report,
                    applicant=request.user,
                    is_reissue=True  # Assuming you have this field to distinguish reissues
                )
                
                reissue_data = {
                    'first_name': reissue_application.first_name,
                    'last_name': reissue_application.last_name,
                    'appointment_location': reissue_application.appointment_location,
                    'appointment_day': reissue_application.appointment_day,
                    'appointment_date': reissue_application.appointment_date,
                    'appointment_time': reissue_application.appointment_time,
                }
                return Response(reissue_data, status=status.HTTP_201_CREATED)
            
            except LicenseApplication.DoesNotExist:
                return Response({"detail": "No existing license found with the provided ID."}, status=status.HTTP_404_NOT_FOUND)
            
            except Exception as e:
                return Response({"detail": f"Failed to create reissue application: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)