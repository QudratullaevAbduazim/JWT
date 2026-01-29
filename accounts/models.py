from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from conf.settings import EXPIRATION_TIME_EMAIL
# Create your models here.

class VerifyCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    is_active = models.BooleanField(default=False)
    expiration_time = models.DateTimeField
    
    
    def __str__(self):
        return f"{self.user.username}: {self.code}"
        
    def save(self, *args, **kwargs):
        self.expiration_time = datetime.now() + timedelta(minutes=EXPIRATION_TIME_EMAIL)
        return super().save(*args, **kwargs)     
        
        