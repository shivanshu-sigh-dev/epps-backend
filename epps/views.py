from rest_framework import viewsets
from .models import Patient, Prescription, DrugInformation, UploadedImage
from .serializers import PatientSerializer, PrescriptionSerializer, DrugInformationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import FileResponse, Http404
from .azure_ocr import AzureOCR
from .azure_openai_utils import AzureOpenAIUtils
import os
import json

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

class PrescriptionByPatientViewSet(viewsets.ViewSet):
    def list(self, request, patient=None):
        if patient is not None:
            prescriptions = Prescription.objects.filter(patient=patient)
            if prescriptions.exists():
                serializer = PrescriptionSerializer(prescriptions, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No prescriptions found for this patient"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Patient ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
class DrugInformationViewSet(viewsets.ModelViewSet):
    queryset = DrugInformation.objects.all()
    serializer_class = DrugInformationSerializer

class DrugInformationByPrescriptionViewSet(viewsets.ViewSet):
    def list(self, request, prescription=None):
        if prescription is not None:
            drug_information = DrugInformation.objects.filter(prescription=prescription)
            if drug_information.exists():
                serializer = DrugInformationSerializer(drug_information, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No drug information found for this prescription"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Prescription ID is required"}, status=status.HTTP_400_BAD_REQUEST)


class MultipleImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')  # Get list of uploaded images
        image_urls = []
        
        for image in images:
            uploaded_image = UploadedImage.objects.create(image=image)  # Save each image
            image_url = os.path.join(settings.MEDIA_URL, uploaded_image.image.name)
            image_urls.append(image_url)
        
        d_info = self.extract_drug_information(image_urls)
        return Response({"d_info": d_info}, status=status.HTTP_201_CREATED)
    
    def extract_drug_information(self, image_urls):
        d_info = []
        for image_url in image_urls:
            ocr = AzureOCR((image_url[1:]).replace("/", "\\"))
            extracted_text = ocr.extract_text()
            if extracted_text != []:
                prescription_data = AzureOpenAIUtils.parse_prescription(extracted_text)
                d_info.append({
                    "image_url": image_url,
                    "prescription_data": prescription_data
                })
        return d_info
                
def get_prescription_image(request, prescription_id):
    try:
        # Get the prescription object
        prescription = Prescription.objects.get(id=prescription_id)
        image_path = prescription.image_url
        image_path = image_path[1:].replace("/", "\\")
        # Check if the file exists on disk
        if not os.path.exists(image_path):
            raise Http404("Prescription image not found")
        
        file_name = os.path.basename(image_path)
        # Open the image file
        response = FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
        # Set the 'Content-Disposition' header to force download with the correct filename
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        
        return response
    
    except Prescription.DoesNotExist:
        raise Http404("Prescription not found")
            
