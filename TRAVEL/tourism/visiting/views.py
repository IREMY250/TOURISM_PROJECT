from .serializers import user_serializers,Profile_serializers,user_profile_serializers,Activity_serializers,Booking_serializers,Book_activity_serializers
from django.contrib.auth.models import User
from .models import User_Profile,Activity,Booking,Book_activity
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def signup(request):
    input=request.data

    user_data={
        'username':input.get('username',None),
        'email':input.get('email',None),
        'password':make_password(input.get('password',None))
        
    }

    user_profile_data={
        'company_name':input.get('company_name',None),
        'profile_picture':input.get('profile_picture',None),
        'address':input.get('address',None),
        'bio':input.get('bio',None),
        'phone_number':input.get('phone_number',None),
        'city':input.get('city',None),
        'country':input.get('country',None),
    }



    serializer_for_user= user_serializers(data=user_data)
    serializer_for_user_profile=Profile_serializers(data=user_profile_data)

    user_valid=serializer_for_user.is_valid()
    user_profile_valid=serializer_for_user_profile.is_valid()


    if user_valid and user_profile_valid :
        user=serializer_for_user.save()
        serializer_for_user_profile.save(user=user)

        response_data={

            'for_user':serializer_for_user.data,
            'for_user_profile':serializer_for_user_profile.data,

        }
        return JsonResponse(response_data,status=status.HTTP_201_CREATED)
    errors= {

        'user_errors': serializer_for_user.errors,
        'profile_errors': serializer_for_user_profile.errors
        
         }
    return JsonResponse(errors,status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def login(request):
    take=request.data
    in_username=take.get('username',None)
    in_password=take.get('password',None)
    get_user=authenticate(username=in_username,password=in_password)
    if get_user:
        token, created= Token.objects.get_or_create(user=get_user)
        serializer=user_serializers(get_user)
        return JsonResponse(
            {
            'message':'logged in successfully',
            'user':serializer.data,
            'token':token.key
            }
            )
    
    return JsonResponse ({"message":"INVALID PASSWORD OR USERNAME"}, status = status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    get_token = Token.objects.get(user=request.user)
    get_token.delete()
    return JsonResponse({"message": "Logged out successfully"}, status=status.HTTP_200_OK)






@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def listusers(request):
    get_user=User_Profile.objects.all()
    serializer=user_profile_serializers(get_user,many=True)
    return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False)



@api_view(['DELETE'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteusers(request):
    take=request.data
    id_to_delete = take.get('id',None)
    do_delete=User.objects.get(id=id_to_delete)
    do_delete.delete()
    return JsonResponse ({"message":"deleted successfully"})


@api_view(['PUT'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    take=request.data
    id_to_update=take.get('id',None)
    do_update=User.objects.get(id=id_to_update)
    serializer=user_serializers(do_update,data=take,partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):
    take=request.data
    id_to_update=take.get('id',None)
    do_update=User_Profile.objects.get(id=id_to_update)
    serializer=user_profile_serializers(do_update,data=take,partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)





@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_activity(request):
    take=request.data
    get_user=request.user
    serializer=Activity_serializers(data=take)
    if serializer.is_valid():
        serializer.save(company=get_user)
        return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_activity(request):
    activities=Activity.objects.all()
    serializer=Activity_serializers(activities,many=True)
    return JsonResponse (serializer.data,status=status.HTTP_200_OK,safe=False)




@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_activity(request):
    get_user=request.user
    get_activity=Activity.objects.filter(company=get_user)
    serializer=Activity_serializers(get_activity,many=True)
    return JsonResponse (serializer.data,status=status.HTTP_201_CREATED,safe=False)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_activity(request):
    take=request.data
    id_to_update=take.get('id',None)
    do_update=Activity.objects.get(id=id_to_update)
    serializer=Activity_serializers(do_update,data=take,partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)



@api_view(['DELETE'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_activity(request):
    take=request.data
    id_to_delete = take.get('id',None)
    do_delete=Activity.objects.get(id=id_to_delete)
    do_delete.delete()
    return JsonResponse ({"message":"deleted successfully"})



@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def Booking(request):
    take=request.data
    activities=take.get('activities',[])

    credentials_booked={
        'customer_name':take.get('customer_name',None),
        'address':take.get('address',None),
        'national_id':take.get('national_id',None),
        'passport':take.get('passport',None),
        'phone_number':take.get('phone_number',None),
        'date':take.get('date',None),
    }

    serializer_credentials_booked= Booking_serializers(data=credentials_booked)
    if serializer_credentials_booked.is_valid():
        instance_of_credentials=serializer_credentials_booked.save()
    else:
         return JsonResponse(serializer_credentials_booked.errors, status=status.HTTP_400_BAD_REQUEST)
    
    for activity in activities:
        act_id=activity.get('id',None)
        slots=activity.get('booked_slots',None)
        get_activity=Activity.objects.get(id=act_id)
       
        
        booked_activity={
            'booking':instance_of_credentials.id,
            'activity':get_activity.id,
            'booked_slots':slots,
        }
        serializer_booked_activity=Book_activity_serializers(data=booked_activity)
        if serializer_booked_activity.is_valid():
            serializer_booked_activity.save()
            if not get_activity.available_slots == 'null':
                get_activity.available_slots=get_activity.available_slots - slots
                get_activity.save()
        else:
         return JsonResponse(serializer_booked_activity.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse (serializer_credentials_booked.data,status=status.HTTP_200_OK)














@api_view(['GET'])
def endpoints(request):
    return Response(
        [
            "http://127.0.0.1:8000/signup/",
            "http://127.0.0.1:8000/login/",
            "http://127.0.0.1:8000/logout/",
            "http://127.0.0.1:8000/listusers/",
            "http://127.0.0.1:8000/deleteusers/",
            "http://127.0.0.1:8000/updateusers/",
            "http://127.0.0.1:8000/updateprofile/",
            "http://127.0.0.1:8000/createactivity/",
            "http://127.0.0.1:8000/listactivity/",
            "http://127.0.0.1:8000/listuseractivity/",
            "http://127.0.0.1:8000/updateactivity/",
            "http://127.0.0.1:8000/deleteactivity/",
            "http://127.0.0.1:8000/booking/",
        ]
    )