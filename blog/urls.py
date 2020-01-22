from django.urls import path 
from . import views, forms
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.contrib.auth import views as v

urlpatterns = [
    path('', views.cons_list, name='cons_list'),
    path('suggs/', views.post_list, name='suggs_list'),
    path('cons/<int:pk>/', views.cons_detail, name='consultation_detail'),
    path('sugg/<int:pk>/', views.post_detail, name='post_detail'),
    path('sugg/new/', views.post_new, name='sugg_new'),
    path('cons/<int:pk>/edit/', views.cons_edit, name='consultation_edit'),
    path('sugg/<int:pk>/edit/', views.post_edit, name='post_edit'),
    # path('user/new/', views.user_new, name='user_new'),
    path('cons/new/', views.cons_new, name='consultation_new'),
    path('signup/', views.user_new, name='signup'),
    # path('signup/', views.signup, name='signup'),
    # path('login/', forms.LoginFormView.as_view(), name='login'),
    path('login/', v.LoginView.as_view(), name='login'),
]
