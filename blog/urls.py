from django.urls import path 
from . import views
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    path('', views.cons_list, name='cons_list'),
    path('cons/<int:pk>/', views.cons_detail, name='consultation_detail'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('cons/<int:pk>/edit/', views.cons_edit, name='consultation_edit'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('user/new/', views.user_new, name='user_new'),
    path('cons/new/', views.cons_new, name='consultation_new'),
    # url('user/auth', views.pagelogin, name='user_auth'),
]