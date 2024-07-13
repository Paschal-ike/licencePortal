from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# class LicenseApplicationManager(models.Manager):
    
  
#     def get_user_details_by_licence_id(self, licence_id):
#         try:
#             return self.get(licence_id=licence_id)
#         except self.model.DoesNotExist:
#             return None
#     def create_reissue_application(self, licence_id, affidavit_police_report, applicant):
#         return self.create(
#             licence_id=licence_id,
#             affidavit_police_report=affidavit_police_report,
#             applicant=applicant
#         )


class LicenseApplication(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        
    ]

    APPLICATION_TYPE_CHOICES = [
        ('new', 'New Application'),
        ('renewal', 'Renewal'),
        ('reissue', 'Reissue'),
    ]

    VEHICLE_TYPE_CHOICES = [
        ('motor_vehicle', 'Motor Vehicle'),
        ('motorcycle_tricycle', 'Motorcycle/Tricycle'),
    ]
    
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
    ]
    applicant = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    mothers_maiden_name = models.CharField(max_length=100)
    nin = models.CharField(max_length=20)
    driving_school_certificate_number = models.CharField(max_length=50, blank=True, null=True)
    passport_photo = models.ImageField(upload_to='passport_photos/')
    affidavit_police_report = models.ImageField(upload_to='affidavits/', blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    state_of_residence = models.CharField(max_length=100)
    local_govt_area = models.CharField(max_length=100)
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPE_CHOICES)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    licence_id = models.CharField(max_length=50, blank=True, null=True ,unique=True)
    appointment_location = models.CharField(max_length=255)
    appointment_day = models.CharField(max_length=20, choices=DAY_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    # Date fields for different application types
    date_of_issuance = models.DateField(blank=True, null=True)
    date_of_renewal = models.DateField(blank=True, null=True)
    date_of_reissuance = models.DateField(blank=True, null=True)
    
    # applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # objects = LicenseApplicationManager()
    

    def __str__(self):
        return f"{self.get_application_type_display()} - {self.first_name} {self.last_name} - {self.nin}"


