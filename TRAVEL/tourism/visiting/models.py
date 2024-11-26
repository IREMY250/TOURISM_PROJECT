from django.db import models
from django.contrib.auth.models import User




class User_Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=250)
    profile_picture=models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bio=models.TextField(blank=True,null=True)
    phone_number=models.CharField(max_length=25)
    city=models.CharField(max_length=250,null=True,blank=True)
    country=models.CharField(max_length=250,null=True,blank=True)

class Activity(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_slots = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    customer_name= models.CharField(max_length=255)
    address=models.TextField(blank=True, null=True)
    national_id=models.IntegerField(null=True)
    passport=models.IntegerField(null=True)
    phone_number=models.CharField(max_length=25)
    date = models.DateField()

class Book_activity(models.Model):
    booking= models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='activities')
    activity=models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='activities')
    booked_slots = models.IntegerField(null=True, blank=True)


class Review(models.Model):
    reviewer=models.CharField(max_length=255)
    rate=models.IntegerField()
    message=models.TextField()
    

 
   