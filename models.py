from django.db import models
import datetime

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, default=datetime.datetime.now, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=200)  # Path to the image stored in Azure Blob
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.name}"

class DrugInformation(models.Model):
    id = models.AutoField(primary_key=True)
    prescription = models.ForeignKey(Prescription, default=datetime.datetime.now, on_delete=models.CASCADE)
    drug_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    strength = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.drug_name} in {self.prescription}"

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')  # Automatically saves to /media/uploads
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.image.name
