from rest_framework import serializers
from .models import LicenseApplication

class LicenseApplicationSerializer(serializers.ModelSerializer):
    passport_photo = serializers.ImageField()

    class Meta:
        model = LicenseApplication
        exclude = ['licence_id', 'date_of_issuance', 'date_of_renewal', 'date_of_reissuance', 'applicant']
    def validate(self, data):
        application_type = data.get('application_type')

        if application_type == 'new':
            if 'affidavit_police_report' in data:
                raise serializers.ValidationError("Affidavit/police report should not be provided for a new application.")
            if 'date_of_issuance' in data or 'date_of_renewal' in data or 'date_of_reissuance' in data:
                raise serializers.ValidationError("Date fields should not be provided for a new application.")
            if 'license_number' in data:
                raise serializers.ValidationError("License number should not be provided for a new application.")
        
        elif application_type == 'renewal':
            if 'affidavit_police_report' in data:
                raise serializers.ValidationError("Affidavit/police report should not be provided for a renewal application.")
            if 'date_of_issuance' not in data:
                raise serializers.ValidationError("Date of issuance is required for a renewal application.")
            if 'licence_number' not in data:
                raise serializers.ValidationError("Licence number is required for a renewal application.")
        elif application_type == 'reissue':
            if 'affidavit_police_report' not in data:
                raise serializers.ValidationError("Affidavit/police report is required for a reissue application.")
            if 'date_of_reissuance' not in data:
                raise serializers.ValidationError("Date of reissuance is required for a reissue application.")
            if 'licence_number' not in data:
                raise serializers.ValidationError("Licence number is required for a reissue application.")

        return data
    

class RenewalApplicationSerializer(serializers.Serializer):
    licence_id = serializers.CharField(max_length=50)

class ReissueApplicationSerializer(serializers.Serializer):
    licence_id = serializers.CharField(max_length=50)
    affidavit_police_report = serializers.ImageField()
