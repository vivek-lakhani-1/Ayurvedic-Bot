from django.db import models

class Register_Data(models.Model):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    is_verified = models.BooleanField()
    
    def __str__(self):
        return self.email
    
    
    
