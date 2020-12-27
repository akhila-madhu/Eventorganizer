from django.contrib import admin
from django.urls import path,include
from django.views import generic
from events.views import (
EventListView,home,event_detail,AddEventCreateView,UpdateEventView,Login,register_user,contactus,logout_user
)
from events.api.views import EventViewSet,LoginView,SignUpView, UserProfileApiView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'api-event', EventViewSet, basename='event')

urlpatterns = [
    path('home/',home),
    path('contactus/',contactus),
    path('login/',Login.as_view()),
    path('logout',logout_user,name="logout"),
    path('register/',register_user,name='register'),
    path('Eventlist', EventListView.as_view(),name='Eventlist'),
    path('event_detail/<int:event_id>',event_detail,name='event_detail'),
    path('add_event', AddEventCreateView.as_view(),name='add_event'),
    path('update_event/<int:pk>', UpdateEventView.as_view(),name='update_event'),
    #path('user-profile', UserProfileView.as_view()),

    path('api-login/', LoginView.as_view()),
    path('api-signup/', SignUpView.as_view()),
    path('api-user-profile/', UserProfileApiView.as_view()),


]  + router.urls

