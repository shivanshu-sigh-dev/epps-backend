from openai import AzureOpenAI
from django.conf import settings
import json

class AzureOpenAIUtils:
        
    def parse_prescription(prescription_text):
        openai_client = AzureOpenAI(api_key=settings.AZURE_OPENAI_API_KEY, api_version=settings.AZURE_OPENAI_API_VERSION, azure_endpoint=settings.AZURE_OPENAI_ENDPOINT)
        prompt = f"""
        Here is the extracted text from prescription:
        {prescription_text}
        
        Please parse the extracted text to identify the medicine names and dosages mentioned in the prescription.
        """
        
        response = openai_client.chat.completions.create(
            model=settings.AZURE_OPENAI_MODEL_NAME, 
            max_tokens=1500,
            temperature=0.5,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant designed to perform analysis on text to identify medicine names. You take text extracted from a prescription as input and provide the medicine names and doges mentioned in the prescription."
                }, {
                    "role": "system",
                    "content": """You format the parsed data as a JSON object with the following structure:
                    {
                        "NAME": "The name of the medicine",
                        "DOSAGE": "The dosage of the medicine",
                        "STRENGTH": "The strength of the medicine",
                        "DURATION": "The duration for which the medicine should be taken",
                        "FREQUENCY": "The frequency at which the medicine should be taken"
                    }
                    """
                }, {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return json.loads(response.choices[0].message.content.replace("```json", "").replace("```", "").strip()) 
    