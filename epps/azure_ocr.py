from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from django.conf import settings

import time

class AzureOCR:
    def __init__(self, image_path):
        self.image_path = image_path
        self.computervision_client = ComputerVisionClient(settings.AZURE_OCR_MODEL_URL, CognitiveServicesCredentials(settings.AZURE_OCR_MODEL_API_KEY))

    def extract_text(self):
        extracted_text = []
        with open(self.image_path, "rb") as image_stream:
            # Call the API with the image stream and raw response (for operation location)
            read_response = self.computervision_client.read_in_stream(image_stream, raw=True)

            # Get the operation location (URL with an ID at the end) from the response
            read_operation_location = read_response.headers["Operation-Location"]

            # Grab the ID from the URL
            operation_id = read_operation_location.split("/")[-1]

            # Call the "GET" API and wait for the results
            while True:
                read_result = self.computervision_client.get_read_result(operation_id)
                if read_result.status not in ['notStarted', 'running']:
                    break
                time.sleep(1)

            # Print the detected text, line by line
            if read_result.status == OperationStatusCodes.succeeded:
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        extracted_text.append(line.text)
        
        return extracted_text