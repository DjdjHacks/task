from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class data(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	image=models.ImageField(upload_to='store_category',default='noimage.jpg', blank=True, null=True)
	date=models.DateTimeField(auto_now_add=True,editable=True)
