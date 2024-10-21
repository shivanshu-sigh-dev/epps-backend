from django.contrib import admin
from .models import Patient, Prescription, DrugInformation, UploadedImage

admin.site.register(Patient)
admin.site.register(Prescription)
admin.site.register(DrugInformation)
admin.site.register(UploadedImage)