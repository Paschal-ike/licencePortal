from rest_framework import serializers
from application.models import LicenseApplication

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseApplication
        fields = [
            'first_name', 'last_name', 'middle_name', 'gender', 'date_of_birth',
            'email', 'phone_number', 'street_address', 'state_of_residence',
            'local_govt_area', 'licence_id', 'application_type', 'vehicle_type',
            'date_of_issuance', 'date_of_renewal', 'date_of_reissuance'
        ]
        read_only_fields = ['licence_id', 'application_type', 'vehicle_type',
                            'date_of_issuance', 'date_of_renewal', 'date_of_reissuance']