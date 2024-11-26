
from rest_framework import serializers
from .models import User_Profile,Activity,Booking,Book_activity,Review
from django.contrib.auth.models import User




class user_serializers(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','username','email','password']

class Profile_serializers(serializers.ModelSerializer):
    class Meta:
        model = User_Profile
        fields= [ 'id','company_name','profile_picture','address','bio','phone_number','city','country']



class user_profile_serializers(serializers.ModelSerializer):
    user=user_serializers()
    class Meta:
       model = User_Profile
       fields= [ 'id','company_name','profile_picture','address','bio','phone_number','city','country',"user"]


class Activity_serializers(serializers.ModelSerializer):
    class Meta:
       model = Activity
       fields= [ 'id','activity_name','description','location','price','available_slots','date']



class Booking_serializers(serializers.ModelSerializer):
    class Meta:
       model = Booking
       fields= [ 'id','customer_name','address','national_id','passport','phone_number','date']


class Book_activity_serializers(serializers.ModelSerializer):
    class Meta:
       model = Book_activity
       fields= [ 'id','booking','activity','booked_slots']



class Review_serializers(serializers.ModelSerializer):
    class Meta:
       model = Review
       fields= [ 'id','reviewer','rate','message']