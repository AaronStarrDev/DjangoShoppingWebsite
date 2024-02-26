from django.contrib import admin
from . import models

##########################################
#   SITE REGISTERS
##########################################

# Model for Patient
admin.site.register(models.Patient, admin.ModelAdmin)

# Model for Administrator
admin.site.register(models.Administrator, admin.ModelAdmin)

# Model for Doctor
admin.site.register(models.Doctor, admin.ModelAdmin)

# Model for Nurse
admin.site.register(models.Nurse, admin.ModelAdmin)

# Model for Hospital
admin.site.register(models.Hospital, admin.ModelAdmin)

# Model for Appointment
admin.site.register(models.Appointment, admin.ModelAdmin)

# Model for Admission
admin.site.register(models.Admission, admin.ModelAdmin)

# Model for Prescription
admin.site.register(models.Prescription, admin.ModelAdmin)

# Model for Drug
admin.site.register(models.Drug, admin.ModelAdmin)