from rest_framework import serializers
from .models import Register_Data
from rest_framework import status

class Serializingdata(serializers.ModelSerializer):
    class Meta:
        model = Register_Data
        fields = ['email','fullname','password','is_verified']
    
    def validate(self,data):
        # if(len(str(data['Phone_No']))!=10):
        #     raise serializers.ValidationError({'error':'Oops! The provided number is not a valid 10-digit phone number. Please make sure to enter a 10-digit phone number for us to assist you. 📞🔢'})
        if(not str(data['email']).endswith('gmail.com')):
            raise serializers.ValidationError({'error':'Sorry, but the email provided is not valid. Please provide a Gmail email address for further assistance. 📮🔒'})
        elif(data['fullname'] == ""):
            raise serializers.ValidationError({'error':'Provide us your Full Name.'})
        return data