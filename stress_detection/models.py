from django.db import models


class register(models.Model): 
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    password = models.CharField(max_length=150)  
    status = models.CharField(max_length=150)  
  
  
class remedy(models.Model): 
    name = models.CharField(max_length=150)
    emotion = models.CharField(max_length=150)
    stress_level= models.CharField(max_length=150)
    music = models.CharField(max_length=150)
    video = models.CharField(max_length=150)
class doctor(models.Model):
    name=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    phone=models.CharField(max_length=150)
    address=models.CharField(max_length=150)
    age=models.CharField(max_length=150)
    password=models.CharField(max_length=150)
    specialization=models.CharField(max_length=150)
    experience=models.CharField(max_length=150)    
class consult(models.Model):
    did=models.CharField(max_length=150)
    uid=models.CharField(max_length=150)
    date=models.CharField(max_length=150)
    des=models.CharField(max_length=150)
    file=models.CharField(max_length=150)
    status=models.CharField(max_length=150)
    medicine=models.CharField(max_length=150)
    prescription=models.CharField(max_length=150)    

class result_tbl(models.Model):
    user=models.CharField(max_length=150)
    uid=models.CharField(max_length=150)
    emotion=models.CharField(max_length=150)
    stress=models.CharField(max_length=150)
    mode=models.CharField(max_length=150)


class upload(models.Model):
    user_id=models.CharField(max_length=150)
    name=models.CharField(max_length=150)
    result=models.CharField(max_length=150)
      