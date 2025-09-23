"""
URL configuration for skillbridge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_page),
    path('registration_service/', views.registration_service, name='registration_service'),
    path('loginpost/', views.loginpost),



    path('admin_home/', views.admin_home),
    path('aview_complaints/', views.aview_complaints),
    path('reply_complaint/<id>/', views.reply_complaint),
    path('view_user/', views.view_user),
    path('view_service/', views.view_service),
    path('verify_service/', views.verify_service),

    path('view_complaints/', views.view_complaints, name='view_complaints'),
    path('send_reply/<int:complaint_id>/', views.send_reply, name='send_reply'),
    path('accept_service/<id>', views.accept_service),
    path('reject_service/<id>', views.reject_service),


    path('service_home/', views.service_home),
    path('view_profile/', views.view_profile),
    path('service_view_works_request/', views.service_view_works_request),
    path('update_profile/', views.update_profile),
    path("approve_request/", views.approve_request ),
    path("reject_request/<id>/", views.reject_request ),

    path("view_works/", views.view_works),
    path("add_work/", views.add_work),
    path("update_work1/", views.update_work1),
    path("update_work/<int:work_id>/", views.update_work),
    path("delete_work/<int:work_id>/", views.delete_work),

    path("user_register/", views.user_register),
    path("user_home/", views.user_home),
    path("user_view_works/", views.user_view_works),
    path("request_work/", views.request_work),
    path("user_view_works_request/", views.user_view_works_request),


    path("view_complaints/", views.view_complaints),
    path("add_complaint/", views.add_complaint),
    path("delete_complaint/<int:comp_id>/", views.delete_complaint),

    path("view_complaints1/", views.view_complaints1),
    path("add_complaint1/", views.add_complaint1),
    path("delete_complaint1/<int:comp_id>/", views.delete_complaint1),





    path("chat_view_service/<id>", views.chat_view_service),
    path("chat_view/", views.chat_view),
    path("chat_send/<msg>", views.chat_send),


]
