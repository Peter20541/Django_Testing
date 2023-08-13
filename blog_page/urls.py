from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name = 'home-page'),
    path('register/',views.user_register, name = 'register-page'),
    path('post_detail/<str:pk>/',views.post_detail, name = 'post_detail-page'),
    path('login/',views.user_login, name ='login-page'),
    path('delete/<str:pk>/',views.delete_post, name ='delete_post-page'),
    path('update/<str:pk>/',views.update_post, name ='update_post-page'),
    path('logout/',views.user_logout, name ='logout-page'),
    path('create_post/',views.user_create_post, name ='create-post-page'),
    path('user_profile/',views.user_profile, name ='profile-page'),
]


