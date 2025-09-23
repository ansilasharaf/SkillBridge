from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.





class User_Table(models.Model):
    LOGIN= models.ForeignKey(User,on_delete=models.CASCADE)
    name= models.CharField(max_length=200)
    phoneno= models.CharField(max_length=12)
    place= models.CharField(max_length=200)
    post= models.CharField(max_length=200)
    pin= models.CharField(max_length=8)
    email= models.CharField(max_length=200)
    photo= models.FileField()
    status= models.CharField(max_length=200,default="user")

class Service_Table(models.Model):
    LOGIN= models.ForeignKey(User,on_delete=models.CASCADE)
    name= models.CharField(max_length=200)
    phoneno= models.CharField(max_length=12)
    place= models.CharField(max_length=200)
    post= models.CharField(max_length=200)
    pin= models.CharField(max_length=8)
    email= models.CharField(max_length=200)
    photo= models.FileField()
    status= models.CharField(max_length=200,default="pending")


class Work_Table(models.Model):
    SERVICE= models.ForeignKey(Service_Table,on_delete=models.CASCADE)
    title= models.CharField(max_length=200)
    description= models.CharField(max_length=12)
    photo= models.FileField()
    price= models.FloatField()
    date= models.DateField()


class Request_Table(models.Model):
    WORK= models.ForeignKey(Work_Table,on_delete=models.CASCADE)
    USER= models.ForeignKey(User_Table,on_delete=models.CASCADE)
    details= models.CharField(max_length=100)
    date= models.DateField()
    due_date= models.DateField()
    price=models.FloatField()
    status=models.CharField(max_length=15)



class Rating_Table(models.Model):
    REQUEST= models.ForeignKey(Request_Table,on_delete=models.CASCADE)
    feedback= models.CharField(max_length=200)
    date= models.DateField()
    rating=models.FloatField()



class Complaint_Table(models.Model):
    LOGIN= models.ForeignKey(User,on_delete=models.CASCADE)
    complaint= models.CharField(max_length=200)
    date= models.DateField()
    reply=models.CharField(max_length=200)

class Chat_Table(models.Model):
    FROM= models.ForeignKey(User,on_delete=models.CASCADE,related_name='fromid')
    TO= models.ForeignKey(User,on_delete=models.CASCADE,related_name='toid')
    message= models.CharField(max_length=200)
    date= models.DateField()
    status=models.CharField(max_length=200)



