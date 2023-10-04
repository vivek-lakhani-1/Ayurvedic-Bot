from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import response,status
import base64
from PIL import Image
from io import BytesIO
import requests

def base64_to_image(base64_string, output_file):
    decoded_data = base64.b64decode(base64_string)
    with open(output_file, "wb") as f:
        f.write(decoded_data)
        
@api_view(['POST'])
def image_process(request):
    print("Got")
    path = str(request.data['base64String'])
    data = path.split(",")[1]
    bytes_decoded = base64.b64decode(data)
    img = Image.open(BytesIO(bytes_decoded))
    img.save("Data/saved_image.jpg")
    API_URL = "https://api-inference.huggingface.co/models/Jayanth2002/swin-base-patch4-window7-224-finetuned-SkinDisease"
    headers = {"Authorization": "Bearer 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"}
    def query(filename):
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()
    ans = query("Data/saved_image.jpg")
    if(ans[0]['score']>=0.30):
        return response.Response({'status':200,'message':ans[0]['label']},status=status.HTTP_200_OK)         
    else:
        return response.Response({'status':200,'message':"No Disease"},status=status.HTTP_200_OK)         