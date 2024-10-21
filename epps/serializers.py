from rest_framework import serializers
from .models import Patient, Prescription, DrugInformation, UploadedImage

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

class DrugInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugInformation
        fields = '__all__'

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ['id', 'image', 'uploaded_at']
