from django.contrib import admin
from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('dashboard/<int:id>',views.dashboard, name = 'dashboard'),
    path('login/', views.signin, name = 'signin'),
    path('logout/', views.logouts, name = 'logout'),
    path('add_post/', views.addPost, name='addpost'),
    path('changeImage/', views.changeImage, name='imagechange'),
    path('posts/<int:id>', views.yourpost, name = 'posts'),
    path('edit_post/<slug:slug>', views.editpost, name='editpost'),
    path('profile/',views.profile_edit, name='profile_edit'),
    path('biddingdetails/<int:id>', views.bidding_details, name = 'biddingdetails'),
    path('follow/<int:id>', views.follow, name='follow'),
    path('verify/<str:token>/', views.verifyaccount, name='verifyaccount'),
    path('resend/',views.resend_the_mail, name='resend'),


]