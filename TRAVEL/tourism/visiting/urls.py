from django.urls import path
from . views import signup,endpoints,login,logout,listusers,deleteusers,update_user,update_profile,create_activity,list_activity,user_activity,update_activity,delete_activity,Booking,review

urlpatterns=[
    path('',endpoints),
    path('signup/',signup),
    path('login/',login),
    path('logout/',logout),
    path('listusers/',listusers),
    path('deleteusers/',deleteusers),
    path('updateusers/',update_user),
    path('updateprofile/',update_profile),
    path('createactivity/',create_activity),
    path('listactivity/',list_activity),
    path('listuseractivity/',user_activity),
    path('updateactivity/',update_activity),
    path('deleteactivity/',delete_activity),
    path('booking/',Booking),
    path('review/',review),

] 