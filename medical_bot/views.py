import os
from rest_framework import response,status
from rest_framework.decorators import api_view
from decouple import config
import requests

url = config('BOT_URL')
internal_api_url = config('Dev_Url')+'/register/check_register'

def query_search(query):
    data = {
        'query': query
    }

    headers = {
        'Content-Type': 'application/json',
    }

    try:
        resp2 = requests.post(url, json=data, headers=headers)
        if resp2.status_code == 200:
            return resp2.json()['message']
        else:
            return None

    except:
        return None


@api_view(['POST'])
def bot_req(request):
    try:
                data = request.data
                email = data['email']
                query = data['query']
                resp = requests.post(internal_api_url,data={'email': email})
                data = resp.json()
                if(data['msg']):
                    if(data['verified']):
                        result = query_search(query)
                        if(result != None):
                                return response.Response({'status':200,'message':result},status=status.HTTP_200_OK)
                        else:
                                return response.Response({'status':404,'message':'Email is not Valid'})
                    else:
                        return response.Response({'status':200,'message':"Please Verify Your Email Address"})
                else:
                        return response.Response({'status':404,'message':'Email is not Valid'})
    except:
            return response.Response({'status':500,'message':"Error Occured"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
  